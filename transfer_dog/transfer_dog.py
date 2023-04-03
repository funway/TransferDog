#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/30 23:13:56

import sys, logging, logging.config

from PySide6.QtWidgets import QApplication, QMessageBox
from peewee import SqliteDatabase

from transfer_dog.main_window import MainWindow
from transfer_dog.model import Task
from transfer_dog.utility.constants import *


class TransferDog(object):
    """
    单例模式
    """
    # 类成员变量 _instance 用作该类的单例
    _instance = None

    def __new__(cls):
        # 如果还不存在单例对象，则创建单例，并进行初始化
        if cls._instance == None:
            cls._instance = object.__new__(cls)

            cls._instance.logger = logging.getLogger(cls.__name__)
            cls._instance.logger.debug('Create %s singleton', cls.__name__)

            # 在此处进行成员变量的声明与初始化
            cls._instance.db = None
        
        return cls._instance

    def __init__(self):
        """A singleton mode. So do not write initial code in __init__() method, write in __new__() method instead.
        """
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

def run():
    # 生成QApplication主程序
    app = QApplication(sys.argv)

    # 设置即使所有窗口都关闭也不退出程序
    # app.setQuitOnLastWindowClosed(False)

    # 设置日志 logging
    try:
        logging.config.fileConfig(LOGGING_CONFIG)
    except Exception as e:
        logging.exception('load logging config file failed! [%s]', LOGGING_CONFIG)
        QMessageBox.critical(None, '配置文件错误', 'Fail to load logging config: [ %s ]' % LOGGING_CONFIG)
        return -1
    
    # 加载配置文件
    doggy = TransferDog()
    doggy.load_config()

    # 加载 stylesheet
    #   由于 QtDesigner 工具不支持加载外部 qss 文件，所以如果想要在 QtDesigner 中预览样式，
    #   就需要在根节点（比如 QMainWindow）上右键选择 "Change styleSheet"，然后将 qss 文件内容拷贝进去
    with open(RESOURCE_PATH / 'qss/default.qss', 'r') as qss_file:
        qss = qss_file.read()
        app.setStyleSheet(qss)
        # 还可以选择 QT 内建的主题，使用 QStyleFactory.keys() 可以返回可用的 styleName。
        # app.setStyle(QStyleFactory.create(styleName))

    # 生成并显示主窗口
    main_window = MainWindow()
    main_window.show()

    # 进入主程序循环
    return app.exec()