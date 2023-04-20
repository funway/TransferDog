#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/30 23:13:56

import sys, logging, logging.config, threading, time, timeit
from datetime import datetime

import psutil
from croniter import croniter
from peewee import SqliteDatabase

from transfer_dog.utility.constants import *
from transfer_worker.model import Task


class TaskRunningStatus(object):
    def __init__(self, process:psutil.Process=None, last_time:datetime=None, next_time:datetime=None, schedule:str='* * * * *'):
        super(TaskRunningStatus, self).__init__()
        self.process = process
        self.last_time = last_time
        self.next_time = next_time
        self.schedule = schedule
        pass

    def __str__(self):
        s = '[p: {p}, last: {last}, next: {next}, schedule: {sche}], {repr}'.format(
            p = None if self.process is None else self.process.pid,
            last = self.last_time,
            next = self.next_time,
            sche = self.schedule,
            repr = object.__repr__(self)
        )
        return s

    
class TransferDog(object):
    """
    单例模式
    """
    # 类成员变量 _instance 用作该类的单例
    _instance = None

    # 生成单例时需要加锁
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
                    self.tasks = {task.uuid: task for task in Task.select()}
                    self.task_statuses = {}

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
            for task in self.tasks.values():
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

                # 1 如果还没有对应的 task_status， 新建一个
                if task.uuid not in self.task_statuses:
                    self.task_statuses[task.uuid] = TaskRunningStatus(next_time=croniter(task.schedule, now).get_next(datetime), 
                                                                      schedule=task.schedule)
                    self.logger.debug('新建 task status: %s', self.task_statuses[task.uuid])

                status = self.task_statuses[task.uuid]
                
                # 如果保存在 status 中的 schedule 与 task.schedule 不一致，说明用户修改了 task 的 schedule
                # 重新计算任务的下次运行时间
                if task.schedule != status.schedule:
                    status.schedule = task.schedule
                    status.next_time = croniter(task.schedule, now).get_next(datetime)

                # 2 先判断任务是否有关联的任务进程
                if status.process is not None:
                    self.logger.debug('task running status: [p%s], last_time[%s], next_time[%s]', status.process.pid, 
                                    status.last_time, status.next_time)
                    
                    # 2.1 如果任务在运行且已经超时，则杀掉任务进程。进入步骤3
                    if status.process.is_running() and (now.timestamp() - status.process.create_time()) > task.timeout:
                        self.logger.warning('[%s] 任务进程 [p%s] 超时！ kill it!', task.uuid, status.process.pid)
                        status.process.kill()
                    # 2.2 如果任务正在运行且未超时，则跳转到下一个任务
                    elif status.process.is_running():
                        self.logger.debug('[%s] 任务进程 [p%s] 正在运行...', task.uuid, status.process.pid)
                        continue
                    # 2.3 任务不在运行了，进入步骤3
                    else:
                        self.logger.debug('[%s] 任务进程 [p%s] 已结束运行', task.uuid, status.process.pid)
                
                # 3 如果任务已启用（并且当前未运行）
                if task.enabled:
                    # 3.1 还未到计划时间
                    if now.timestamp() < status.next_time.timestamp():
                        self.logger.debug('[%s] 任务未到计划运行时间: %s', task.uuid, status.next_time)
                    # 3.2 已到（或者已超过）计划时间，启动任务子进程，并计算下一次运行时间
                    else:
                        self.logger.info('[%s] 任务 (%s) 已到运行时间，启动任务子进程', task.uuid, task.task_name)
                        # 启动子进程
                        # python3 worker.py --log_config conf/worker_logging.conf -d conf/task.db -i 71b63d312b0a4c7284843033ab7f6b92
                        cmd_line = 'python3 {py_file} --daemon --log_config {log_config} -d {db_file} -i {uuid}'.format(
                            py_file = str(PROJECT_PATH / 'worker.py'),
                            log_config = str(LOGGING_CONFIG.parent / 'worker_logging.conf'),
                            db_file = str(TASK_DB),
                            uuid = task.uuid
                            )
                        self.logger.debug('子进程命令: %s', cmd_line)
                        status.process = psutil.Popen(cmd_line.split())
                        status.next_time = croniter(task.schedule, now).get_next(datetime)
                        status.last_time = datetime.fromtimestamp(status.process.create_time())
                else:
                    self.logger.debug('[%s] 任务未启用', task.uuid)

            # TODO
            # 在这里发送信号告诉 treeview 更新 itemwidget
            # 好像不行，要想发射信号，得把自己变成 QObject 的子类，这会导致单例那里出问题。
            # 更简单，我应该想个办法，直接在 treeview 那里去定时刷新

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