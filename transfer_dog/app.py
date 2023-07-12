#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/13 20:41:06

import sys, logging, logging.config, os, time
from configparser import ConfigParser

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import QTranslator, QLocale

from transfer_dog.transfer_dog import TransferDog
from transfer_dog.utility.constants import *
from transfer_dog.utility.single_app_guard import SingleAppGuard, raise_window
from transfer_dog.view.main_window import MainWindow
import transfer_dog.utility.global_variables as gv


def run():
    # 设置当前工作目录
    os.chdir(PROJECT_PATH)

    # 生成QApplication主程序
    q_app = QApplication(sys.argv)

    # 设置即使所有窗口都关闭也不退出程序
    # q_app.setQuitOnLastWindowClosed(False)

    # 加载配置文件
    load_logging_config()
    load_app_config()
    
    # 确保程序单实例运行
    guard = SingleAppGuard(APP_BUNDLE_ID)

    # 加载翻译器
    gv.translator = QTranslator()
    if gv.translator.load(gv.cfg['DEFAULT']['lang'], directory=str(LANGS_PATH)) is False:
        logging.warning('加载语言文件失败! [%s]', gv.cfg['DEFAULT']['lang'])
    q_app.installTranslator(gv.translator)
    
    # 设置 QApplication 的程序名与版本号
    q_app.setApplicationName(APP_NAME)
    q_app.setApplicationVersion(APP_VERSION)

    # 设置程序运行时窗口图标(使用 python 命令运行的才需要)
    app_icon = QIcon(str(RESOURCE_PATH / 'app_icon/dog.ico'))
    q_app.setWindowIcon(app_icon)

    # 加载 stylesheet
    #   由于 QtDesigner 工具不支持加载外部 qss 文件，所以如果想要在 QtDesigner 中预览样式，
    #   就需要在根节点（比如 QMainWindow）上右键选择 "Change styleSheet"，然后将 qss 文件内容拷贝进去
    qss_file = str(RESOURCE_PATH.joinpath('qss', gv.cfg['DEFAULT']['theme']+'.qss'))
    try:
        with open(qss_file, 'r', encoding='UTF8') as qf:
            qss = qf.read()
            q_app.setStyleSheet(qss)
    except Exception as e:
        logging.exception('Load qss file failed! [%s]', qss_file)
        QMessageBox.warning(None, '无法加载主题文件', '<b>Failed to load [ %s ]</b><br><br>%s' % (qss_file, e))

    # 创建 TransferDog 单例并加载任务配置
    doggy = TransferDog()
        
    # 生成并显示主窗口
    main_window = MainWindow()
    main_window.show()

    q_app.applicationStateChanged.connect(lambda state: on_app_state_changed(state, main_window))

    if guard.is_listening():
        # 当程序有新实例“企图”运行时，唤醒当前的唯一实例
        guard.server.newConnection.connect(lambda: raise_window(main_window))

    # 启动 TransferDog 运行子线程，进行任务调度
    doggy.run()
    
    # 进入 QApplication 事件循环线程（主线程）
    result = q_app.exec()

    # 程序退出前的资源释放操作（Python 的垃圾回收机制会自行释放，没必要手工执行）
    # doggy.stop(True)
    # TransferDog._instance = None
    
    return result

def on_app_state_changed(state, main_window):
    """QApplication.ApplicationState 状态变化时的响应函数

    不同系统，会有不同的情况触发 QApplication 的状态变化
    
    Windows: 鼠标不论左右键点击系统托盘图标，都会触发 ApplicationActive
    macOS: 鼠标点击 dock 栏图标，会触发 ApplicationActive

    Args:
        state (_type_): _description_
        main_window (_type_): _description_
    """

    logging.debug('app state changed: %s', state)
    
    if state == Qt.ApplicationState.ApplicationActive and os.name != 'nt':
        # 针对 macOS 平台，点击 dock 栏程序图标，就会触发 ApplicationState 变成 ApplicationActive
        if QApplication.instance().activeWindow() is None:
            main_window.show()
    pass

def load_logging_config():
    try:
        logging.config.fileConfig(LOGGING_CONFIG, encoding='UTF8')
    except Exception as e:
        logging.exception('Load logging config file failed! [%s]', LOGGING_CONFIG)
        QMessageBox.critical(None, '无法加载日志配置', '<b>Failed to load [ %s ]</b><br><br>%s' % (LOGGING_CONFIG, e))
        sys.exit(2)
    pass

def load_app_config():
    """读取 app.conf 配置文件，并保存在 global_variables.py 模块的 cfg 变量中
    """
    cfg = ConfigParser(defaults={'lang':'en_US', 
                                 'theme':'default'})
    try:
        logging.info('Load app config from: %s', APP_CONFIG)
        assert APP_CONFIG.exists(), '%s not exists!' % APP_CONFIG
        cfg.read(APP_CONFIG)
    except Exception as e:
        logging.exception('Load app config file failed! [%s]', APP_CONFIG)
        QMessageBox.critical(None, '无法加载程序配置', '<b>Failed to load [ %s ]</b><br><br>%s' % (APP_CONFIG, e))
        sys.exit(3)
    
    gv.cfg = cfg
    pass