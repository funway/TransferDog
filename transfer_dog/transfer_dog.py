#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/30 23:13:56

import sys, logging, logging.config, threading, time, timeit

from peewee import SqliteDatabase

from transfer_dog.utility.constants import *
from transfer_worker.model import Task


class TransferDog(object):
    """
    单例模式
    """
    # 类成员变量 _instance 用作该类的单例
    _instance = None
    _lock = threading.Lock()
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
                # 判断 task 是否需要运行
                if task.enabled:

                    pass
                pass

            self.logger.debug('Dog running...')
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