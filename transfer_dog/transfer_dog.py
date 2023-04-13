#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/30 23:13:56

import sys, logging, logging.config, threading

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
                    cls._initialized = True
                    
                    # 在此处进行成员变量的声明与初始化
                    self.logger = logging.getLogger(cls.__name__)
                    self.logger.info('Init %s singleton', cls.__name__)

                    self.db = None
                    self.load_config()
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
