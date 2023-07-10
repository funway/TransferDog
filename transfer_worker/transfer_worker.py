#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/16 10:09:37

import logging, time, importlib, tempfile, os
from pathlib import Path
from datetime import datetime, timedelta

from peewee import OperationalError, SqliteDatabase

from transfer_worker.model.task import Task
from transfer_worker.model.processed import Processed
from transfer_worker.worker.factory import GetterFactory, PutterFactory
from transfer_worker.worker.local_woker import LocalGetter, LocalPutter
from transfer_worker.worker.middle_file import MiddleFile, Abort
import transfer_worker.middleware.nothing as default_middleware


class TransferWorker(object):
    """docstring for TransferWorker."""
    def __init__(self, task_uuid: str, task_db: str, processed_db: str):
        super(TransferWorker, self).__init__()
        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        # 连接 task 数据库
        self.task_db = SqliteDatabase(task_db, autoconnect=True)
        # 绑定模型与数据库
        self.task_db.bind([Task, ])

        # 加载任务
        self.task = self.load_task(task_uuid)

        # 确保 processed 文件的目录存在
        Path(processed_db).parent.mkdir(parents=True, exist_ok=True)

        # 连接 processed 数据库
        self.processed_db = SqliteDatabase(processed_db)
        # 绑定模型与数据库
        self.processed_db.bind([Processed, ])
        # 如果不存在表，则创建表
        self.processed_db.create_tables([Processed], safe=True)
        # 清理过期的处理记录
        self.delete_outdated_processed()

        pass

    def load_task(self, task_uuid) -> Task:
        self.logger.debug('Load task [%s]', task_uuid)

        try:
            task = Task.get_or_none(Task.uuid == task_uuid)
            assert task is not None, 'Can not find the task!'
        except OperationalError as e:
            self.logger.exception('Task 表异常!')
            raise e
        except Exception as e:
            self.logger.exception('无法找任务[%s]!', task_uuid)
            raise e
        finally:
            self.task_db.close()
            pass
        
        return task

    def run(self) -> int:
        """运行作业，根据源地址与目标地址区分如下四种情况：
        1. local  >> local:  
            getter 拷贝 mid_file 到 dest.path 目录下 > middleware > putter 剪切 mid_file > 删除源文件 > 尝试删除 mid_file
        2. local  >> remote: 
            getter 不拷贝 mid_file, mid_file 就是源文件 > middleware > putter 上传文件 > 删除源文件 > 不删除 mid_file
        3. remote >> local: 
            getter 下载 mid_file 到 dest.path 目录下 > middleware > putter 剪切 mid_file > 删除源文件 > 尝试删除 mid_file
        4. remote >> remote: 
            getter 下载 mid_file 到系统 temp 目录下 > middleware > putter 上传文件 > 删除源文件 > 尝试删除 mid_file

        Returns:
            int: 运行结果。0 表示正常结束, 非 0 表示执行异常
        """
        self.logger.info('开始作业 [%s]: %s', self.task.uuid, self.task.task_name)

        # 创建 Getter
        try:
            g = GetterFactory.make_getter(self.task)
        except Exception as e:
            self.logger.exception('Failed to initialize a source Getter')
            return 1
        
        # 创建 Putter
        try:
            p = PutterFactory.make_putter(self.task)
        except Exception as e:
            self.logger.exception('Failed to initialize a destination Putter')
            return 1

        # 创建中间件
        middleware = self.load_middleware()
        
        mid_path = self.resolve_middle_path(g, p)
        
        count = 0

        # 1. Getter.next() 迭代器获取待处理的源文件 > mid_file(source, source_mtime)
        for mid_file in g.next():
            self.logger.debug('next midfile: %s', mid_file)
            
            # 2. 中间件预处理
            if hasattr(middleware, 'pre_process'):
                middleware.pre_process(mid_file, self.task.middleware_arg)
                self.logger.debug('after %s.pre_preocess: %s', middleware.__name__, mid_file)
            
            # 2.1 中间件预处理要求中止操作
            if mid_file.abort != Abort.NO_ABORT:
                self.logger.debug('中间件预处理要求中止操作')
                
                if mid_file.abort == Abort.ABORT_AND_RECORD:
                    self.save_processed(mid_file)
                    count += 1
                
                continue

            # 3. 下载源文件 > mid_file(source, source_mtime, middle)
            g.get(mid_file, mid_path)
            self.logger.debug('got midfile: %s', mid_file)

            # 4. 中间件后处理 > mid_file(source, source_mtime, middle, dest)
            if hasattr(middleware, 'process'):
                middleware.process(mid_file, self.task.middleware_arg)
                self.logger.debug('after %s.process: %s', middleware.__name__, mid_file)
            
            # 4.1 中间件后处理要求中止操作
            if mid_file.abort != Abort.NO_ABORT:
                self.logger.debug('中间件后处理要求中止操作')
                
                if mid_file.abort == Abort.ABORT_AND_RECORD:
                    self.save_processed(mid_file)
                    count += 1
                
                # 确保删除中间文件
                if isinstance(mid_file.middle, Path) and mid_file.middle != g.src_path.joinpath(mid_file.source):
                    mid_file.middle.unlink(missing_ok=True)
                continue
            
            # 兜底设置 dest（如果中间件没有设置 dest 的话）
            if mid_file.dest is None:
                mid_file.dest = mid_file.source

            # 5. 上传文件
            p.put(mid_file)

            # 6. 保存处理记录
            self.save_processed(mid_file)
            count += 1

            # 7. 删除源文件
            if self.task.delete_source:
                g.delete_source(mid_file)
            
            # 8. 删除中间文件
            # 只要 mid_file != sourcefile，都要手动删除中间文件。（即使是 LocalPutter，因为也有可能是下载了，但被 middleware abort 掉了，那么临时文件就还在）
            if isinstance(mid_file.middle, Path) and mid_file.middle != g.src_path.joinpath(mid_file.source):
                mid_file.middle.unlink(missing_ok=True)

        self.logger.info('完成作业 [%s]: %s. 本次共处理文件 %s 个', self.task.uuid, self.task.task_name, count)
        return 0

    def load_middleware(self):
        """加载中间件

        Raises:
            e: _description_
        """
        self.logger.debug('load middleware: %s, arg: %s', self.task.middleware, self.task.middleware_arg)
        try:
            if self.task.middleware is None:
                # middleware = importlib.import_module('.nothing', 'transfer_worker.middleware')
                middleware = default_middleware
            else:
                middleware = importlib.import_module('.%s' % Path(self.task.middleware).stem, 'plugin.middleware')
            
            # 可选地有 process() 函数
            if hasattr(middleware, 'process'):
                assert callable(middleware.process), "'%s.process' is not callable" % middleware.__name__
            
            # 可选地有 pre_process() 函数
            if hasattr(middleware, 'pre_process'):
                assert callable(middleware.pre_process), "'%s.pre_process' is not callable" % middleware.__name__            
        except Exception as e:
            self.logger.exception('加载中间件模块出现异常')
            raise e
        
        self.logger.debug('middleware loaded: %s', middleware.__name__)
        return middleware

    def resolve_middle_path(self, getter, putter):
        """根据源地址与目标地址判断中间临时文件的存放路径
        1. local  >> local:  mid_file 就放 dest.path 目录, mid_path = dest.path
        2. local  >> remote: mid_file 就是源文件, mid_path = None
        3. remote >> local:  mid_file 就放 dest.path 目录, mid_path = dest.path
        4. remote >> remote: mid_file 就放系统的临时目录, mid_path = tempfile.gettempdir()

        Args:
            getter (_type_): _description_
            putter (_type_): _description_

        Returns:
            str: _description_
        """
        if isinstance(putter, LocalPutter):
            return putter.dest_path
        elif isinstance(getter, LocalGetter):
            return None
        else:
            return Path(tempfile.gettempdir())
    
    def save_processed(self, mid_file: MiddleFile):
        self.logger.debug('保存处理记录: (%s, %s)', mid_file.source, mid_file.source_mtime)
        Processed.create(source=mid_file.source, mtime=mid_file.source_mtime, pid=os.getpid())
        pass
    
    def delete_outdated_processed(self):
        outdated = datetime.now() - timedelta(seconds=self.task.processed_reserve_time)
        self.logger.debug('清理过期的 processed 记录( before %s )', outdated)
        
        rows = Processed.delete().where(Processed.processed_at < outdated).execute()
        self.logger.debug('删除 %s 行数据', rows)
        pass