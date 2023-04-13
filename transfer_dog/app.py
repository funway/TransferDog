#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/13 20:41:06

import sys, logging, logging.config

from PySide6.QtWidgets import QApplication, QMessageBox

from transfer_dog.transfer_dog import TransferDog
from transfer_dog.utility.constants import *
from transfer_dog.view.main_window import MainWindow


def run():
    # 生成QApplication主程序
    q_app = QApplication(sys.argv)

    # 设置即使所有窗口都关闭也不退出程序
    # app.setQuitOnLastWindowClosed(False)

    # 设置日志 logging
    try:
        logging.config.fileConfig(LOGGING_CONFIG)
    except Exception as e:
        logging.exception('load logging config file failed! [%s]', LOGGING_CONFIG)
        QMessageBox.critical(None, '配置文件错误', 'Fail to load logging config: [ %s ]' % LOGGING_CONFIG)
        return -1
    
    # 设置 QApplication 的程序名与版本号
    q_app.setApplicationName(APP_NAME)
    q_app.setApplicationVersion(APP_VERSION)
    
    # 创建 TransferDog 单例并加载配置
    doggy = TransferDog()

    # 加载 stylesheet
    #   由于 QtDesigner 工具不支持加载外部 qss 文件，所以如果想要在 QtDesigner 中预览样式，
    #   就需要在根节点（比如 QMainWindow）上右键选择 "Change styleSheet"，然后将 qss 文件内容拷贝进去
    with open(RESOURCE_PATH / 'qss/default.qss', 'r') as qss_file:
        qss = qss_file.read()
        q_app.setStyleSheet(qss)
        # 还可以选择 QT 内建的主题，使用 QStyleFactory.keys() 可以返回可用的 styleName。
        # app.setStyle(QStyleFactory.create(styleName))

    # 生成并显示主窗口
    main_window = MainWindow()
    main_window.show()

    # 进入主程序循环
    return q_app.exec()