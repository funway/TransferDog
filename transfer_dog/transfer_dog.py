#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/30 23:13:56

import sys, logging, logging.config, threading, time, timeit, shlex
from datetime import datetime

import psutil
from croniter import croniter
from peewee import SqliteDatabase
from PySide6 import QtCore
from PySide6.QtGui import QMovie

from transfer_dog.utility.constants import *
from transfer_worker.model import Task


class TransferDog(object):
    """
    单例模式
    """
    # 类成员变量 _instance 用作该类的单例
    _instance = None

    # 生成单例时需要加锁，创建 status.process 时也要加锁
    _lock = threading.Lock()

    # 表示单例是否已经初始化了
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # 创建单例
                    cls._instance = object.__new__(cls)
                    pass
                pass
            pass      
        return cls._instance

    def __init__(self):
        cls = self.__class__
        if not cls._initialized:
            with cls._lock:
                if not cls._initialized:
                    # 在此处进行成员变量的声明与初始化
                    self.logger = logging.getLogger(cls.__name__)
                    self.logger.debug('Init %s singleton', cls.__name__)
                    self.logger.setLevel(logging.INFO)

                    self._stop = False

                    self.db = None
                    self.load_config()
                    
                    # 任务字典 {uuid: task}
                    self.dict_tasks = {}
                    
                    # 任务运行状态的字典 {uuid: TaskStatus}
                    self.dict_task_statuses = {}
                    
                    # 任务 widget 的字典 {uuid: TaskWidget}
                    self.dict_task_widgets = {}

                    # 处于 treeview 可视区域的任务集合 {uuid}
                    self.set_visible_tasks = set()

                    # 所有 taskwidget 共享这个 QMovie 对象，减少内存与 CPU 开销
                    self.running_gif = QMovie(str( RESOURCE_PATH / 'img/running2.gif' ))
                    self.running_gif.setScaledSize(QtCore.QSize(32, 32))
                    self.running_gif.setCacheMode(QMovie.CacheMode.CacheAll)
                    self.running_gif.start()

                    cls._initialized = True
                    pass
                pass
            pass
        pass
    
    def __del__(self):
        self.logger.debug('Delete %s singleton', self.__class__.__name__)
        pass

    def load_config(self, db_file=TASK_DB):
        # 从指定文件创建数据库链接（如果不存在该文件，会主动创建）
        self.db = SqliteDatabase(db_file, autoconnect=False)
        self.db.connect()

        # 将 models 绑定到数据库，并创建对应的数据库表（if not exist）
        models = [Task, ]
        self.db.bind(models)
        self.db.create_tables(models, safe=True)
        pass

    def _run(self):
        self._stop = False
        while not self._stop:
            t1 = timeit.default_timer()
            
            # do your running job
            # create subprocess for task
            for task in self.dict_tasks.values():
                """
                1. 判断上次 task 是否还在运行
                    1.1 如果还在运行且未超时，continue 下一个任务
                    1.2 如果还在运行且已超时，kill it，下一步
                    1.3 如果不在运行，下一步
                2. 判断 task 是否启用
                    2.1 如果启用且到点运行了，启动作业子进程，下一步
                    2.2 如果启用且未到点，下一步
                    2.3 如果未启用，下一步
                """
                self.logger.debug('检查是否需要启动任务 [%s: %s]', task.uuid[-4:], task.task_name)
                now = datetime.now()

                # 1 获取 task status
                status = self.dict_task_statuses[task.uuid]
                
                # 如果保存在 status 中的 schedule 与 task.schedule 不一致，说明用户修改了 task 的 schedule
                # 重新计算任务的下次运行时间
                if status.schedule != task.schedule:
                    self.logger.info('[%s]任务计划变更', task.uuid)
                    status.schedule = task.schedule
                    status.next_time = croniter(task.schedule, now).get_next(datetime)
                    status.need_update = True
                
                # 如果用户修改了 enabled 状态
                if status.enabled != task.enabled:
                    self.logger.info('[%s]enabled 状态变更', task.uuid)
                    status.enabled = task.enabled
                    status.need_update= True
                    # 如果是重启了任务，需要重新计算下一次运行时间
                    if task.enabled:
                        status.next_time = croniter(task.schedule, now).get_next(datetime)

                # 2 先判断任务是否有关联的任务进程
                if status.process is not None:
                    try:
                        # 必须 wait(0) 来处理已退出的子进程，否则子进程会变成僵尸进程（僵尸进程 is_running 也返回 true）
                        status.process.wait(0)
                    except Exception as e:
                        pass
                    
                    self.logger.debug('task subprocess: [%s], next_time: %s', status.process, status.next_time)
                    
                    # 2.1 如果任务在运行且已经超时，则杀掉任务进程。进入步骤3
                    if status.process.is_running() and (now.timestamp() - status.process.create_time()) > task.timeout:
                        self.logger.warning('[%s] 任务进程 [p%s] 超时！ kill it!', task.uuid, status.process.pid)
                        self.kill_task(task.uuid)
                    # 2.2 如果任务正在运行且未超时，则跳转到下一个任务
                    elif status.process.is_running():
                        self.logger.debug('[%s] 任务进程 [p%s] 正在运行...', task.uuid, status.process.pid)
                        if status.need_update:
                            self._update_task_widget(task.uuid)
                        continue
                    # 2.3 任务不在运行了，进入步骤3
                    else:
                        self.logger.info('[%s] 任务进程 [p%s] 已结束运行', task.uuid, status.process.pid)
                        status.process = None
                        status.need_update = True
                
                # 3 如果任务已启用（并且当前未运行）
                if task.enabled:
                    # 3.1 还未到计划时间
                    if now.timestamp() < status.next_time.timestamp():
                        self.logger.debug('[%s] 任务未到计划运行时间: %s', task.uuid, status.next_time)
                    # 3.2 已到（或者已超过）计划时间，启动任务子进程，并计算下一次运行时间
                    else:
                        self.logger.info('[%s] 任务 (%s) 已到运行时间，启动任务子进程', task.uuid, task.task_name)
                        # 启动任务子进程
                        self.start_task(task.uuid)
                else:
                    self.logger.debug('[%s] 任务未启用', task.uuid)

                if status.need_update:
                    self._update_task_widget(task.uuid)

            time.sleep(0.2)

            t2 = timeit.default_timer()
            self.logger.debug(t2 - t1)
            pass
        pass

    def run(self, daemon: bool = True):
        """启动任务调度子线程。对到点运行的任务，启动一个 subprocess 进行处理

        Args:
            daemon (bool, optional): 子线程是否运行在 daemon 模式。Defaults to True.
                如果是，则程序主线程退出后，子线程自动退出；
                如果不是，需要手工调用 stop() 停止子线程，否则子线程、主线程均不会退出。
        """
        running_thread = threading.Thread(target=self._run, daemon=daemon)
        running_thread.start()
        pass

    def stop(self):
        """手动停止任务调度子线程（通过 self._stop 标记位）
        """
        self._stop = True
        pass

    def start_task(self, uuid):
        task = self.dict_tasks[uuid]
        status = self.dict_task_statuses[uuid]

        # python3 worker.py --log_config conf/worker_logging.conf -d conf/task.db -i 71b63d312b0a4c7284843033ab7f6b92
        cmd_line = 'python3 {py_file} --daemon --log_config {log_config} -d {db_file} -i {uuid}'.format(
            py_file = str(PROJECT_PATH / 'worker.py'),
            log_config = str(LOGGING_CONFIG.parent / 'worker_logging.conf'),
            db_file = str(TASK_DB),
            uuid = task.uuid
            )
        self.logger.debug('子进程命令: %s', cmd_line)
        
        args = shlex.split(cmd_line, posix=('win' not in sys.platform))
        self.logger.debug('拆解命令: %s', args)
        
        with __class__._lock:
            if status.process is not None and status.process.is_running():
                self.logger.warning('[%s] 任务进程正在运行', task.task_name)
                return
            
            try:
                status.process = psutil.Popen(args)
            except Exception as e:
                self.logger.exception('无法启动任务子进程: %s', args)
                raise e
            else:
                status.next_time = croniter(task.schedule, datetime.now()).get_next(datetime)
                status.last_time = datetime.fromtimestamp(status.process.create_time())
                status.need_update = True
        pass

    def kill_task(self, uuid):
        status = self.dict_task_statuses[uuid]
        
        if status.process is not None:
            status.process.kill()
            status.process.wait()  # 必须调用 wait() 处理子进程退后保留的信息，否则子进程会变成僵尸进程
        pass

    def hide(self, uuid: str):
        """隐藏 uuid 任务节点

        Args:
            uuid (_type_): task uuid
        """
        self.dict_task_widgets[uuid].hide()
        self.set_visible_tasks.discard(uuid)
        pass

    def update_task_widgets(self):
        """刷新所有处于 treeview 可视区域的 TaskWidget
        """
        self.logger.debug('有 %s 个 task widget 在可视区域', len(self.doggy.set_visible_tasks))
        for task_uuid in self.doggy.set_visible_tasks:
            self._update_task_widget(task_uuid)
        pass
    
    def _update_task_widget(self, task_uuid: str):
        self.logger.info('刷新任务状态 [%s]', task_uuid)
            
        task = self.dict_tasks[task_uuid]
        
        status = self.dict_task_statuses.get(task_uuid)

        widget = self.dict_task_widgets[task_uuid]

        # TODO
        # 如果任务名字有变化，而且正好又是被 搜索 出来标红的 怎么办？
        # if widget.label_title.text() != task.task_name:
        
        # 如果任务未启用
        if not task.enabled:
            self.logger.debug('[%s] 任务未启用', task_uuid)
            widget.task_disabled(status)
        else:
            self.logger.debug('[%s] 任务已启用', task_uuid)
            widget.task_enabled(status)

        # 如果任务在运行
        if status is not None and status.process is not None and status.process.is_running():
            self.logger.debug('[%s] 任务正在运行', task_uuid)
            widget.task_running(movie=self.running_gif)
        else:
            self.logger.debug('[%s] 任务未运行', task_uuid)
            widget.task_stopped()
        
        status.need_update = False
        pass