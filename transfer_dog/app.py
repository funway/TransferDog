#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/13 20:41:06

import sys, logging, logging.config, random

from PySide6.QtWidgets import QApplication, QMessageBox, QStyleFactory

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
        logging.config.fileConfig(LOGGING_CONFIG, encoding='UTF8')
    except Exception as e:
        logging.exception('Load logging config file failed! [%s]', LOGGING_CONFIG)
        QMessageBox.critical(None, '配置文件错误', '<b>Failed to load [ %s ]</b><br><br>%s' % (LOGGING_CONFIG, e))
        return -1
    
    # 设置 QApplication 的程序名与版本号
    q_app.setApplicationName(APP_NAME)
    q_app.setApplicationVersion(APP_VERSION)
    
    # 创建 TransferDog 单例并加载配置
    doggy = TransferDog()

    # 加载 stylesheet
    #   由于 QtDesigner 工具不支持加载外部 qss 文件，所以如果想要在 QtDesigner 中预览样式，
    #   就需要在根节点（比如 QMainWindow）上右键选择 "Change styleSheet"，然后将 qss 文件内容拷贝进去
    qss_file = str(RESOURCE_PATH / 'qss/default.qss')
    try:
        with open(qss_file, 'r', encoding='UTF8') as qf:
            qss = qf.read()
            q_app.setStyleSheet(qss)
    except Exception as e:
        logging.exception('Load qss file failed! [%s]', qss_file)
        QMessageBox.warning(None, '配置文件错误', '<b>Failed to load [ %s ]</b><br><br>%s' % (qss_file, e))
    
    # 生成并显示主窗口
    main_window = MainWindow()
    main_window.show()

    # 启动 TransferDog 运行子线程，进行任务调度
    doggy.run()
    
    # 进入 QApplication 事件循环线程（主线程）
    result = q_app.exec()
    
    return result