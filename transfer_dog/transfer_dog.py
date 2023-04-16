#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/30 23:13:56

import sys, logging, logging.config, threading, time, timeit

from peewee import SqliteDatabase

from transfer_dog.model import Task
from transfer_dog.utility.constants import *


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
                    self.logger.info('Init %s singleton', cls.__name__)

                    self._stop = False

                    self.db = None
                    self.load_config()
                    self.tasks = [task for task in Task.select()]

                    cls._initialized = True
                    pass
                pass
            pass
        pass
    
    def __del__(self):
        self.logger.debug('Delete %s singleton', self.__class__.__name__)
        pass

    def load_config(self, db_file=CONFIG_DB):
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
            for task in self.tasks:
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
            self.logger.info(t2 - t1)
            pass
        pass

    def run(self):
        running_thread = threading.Thread(target=self._run)
        running_thread.start()
        pass

    def stop(self):
        self._stop = True
        pass