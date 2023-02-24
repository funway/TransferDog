#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import os, sys, logging, logging.config

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from peewee import SqliteDatabase
from playhouse.shortcuts import model_to_dict

from utility.constants import *
from model.task import Task
from ui.ui_main_window import Ui_MainWindow
from dialog_task_edit import DialogTaskEdit


class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance' % self.__class__.__name__)
        
        # 定义成员变量
        self.db = None

        # 读取配置文件
        self.load_config()

        # 装载 UI
        self.setupUi(self)
        
        # 绑定信号-槽
        self.actionNewTask.triggered.connect(lambda: self.show_dialog_task_edit(None))

        pass

    def load_config(self, db_file=CONFIG_DB):
        # 从指定文件创建数据库链接（如果不存在该文件，会主动创建）
        self.db = SqliteDatabase(db_file, autoconnect=False)
        self.db.connect()

        # 将 models 绑定到数据库，并创建对应的数据库表（if not exist）
        self.db.bind([Task,])
        self.db.create_tables([Task,], safe=True)

        pass

    def update_UI(self):
        """执行一些无法在 setupUi() 中完成的界面更新
        """
        self.treeView.setHeaderHidden(True)
        pass

    def show_dialog_task_edit(self, task:Task=None):
        self.logger.debug('show dialog_task_edit with task: %s', task)
        
        dialog = DialogTaskEdit(task=task)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.logger.debug("dialog save clicked!")
            task = dialog.retrieve_task()
            self.logger.debug('retrieve task: %s', model_to_dict(task))
            try:
                task.save()
            except Exception as e:
                self.logger.exception('保存任务失败！')
        else:
            self.logger.debug("dialog cancel clicked")
        pass

    def __del__(self):
        self.db.close()
        pass
    

def main(arg=None):
    # 设置工作目录
    os.chdir(BASE_PATH)
    
    # 生成QApplication主程序
    app = QApplication(sys.argv)

    # 设置即使所有窗口都关闭也不退出程序
    # app.setQuitOnLastWindowClosed(False)

    # 设置日志 logging
    try:
        logging.config.fileConfig(LOGGING_CONFIG)
    except Exception as e:
        logging.exception('load logging config file failed! [%s]', LOGGING_CONFIG)
        QMessageBox.critical(None, '配置文件错误', 'Fail to load %s' % LOGGING_CONFIG)
        sys.exit(-1)

    # 加载 stylesheet
    #   由于 QtDesigner 工具不支持加载外部 qss 文件，所以如果想要在 QtDesigner 中预览样式，
    #   就需要在根节点（比如 QMainWindow）上右键选择 "Change styleSheet"，然后将 qss 文件内容拷贝进去
    with open(BASE_PATH + '/ui/resource/qss/default.qss', 'r') as qss_file:
        qss = qss_file.read()
        app.setStyleSheet(qss)
        # 还可以选择 QT 内建的主题，使用 QStyleFactory.keys() 可以返回可用的 styleName。
        # app.setStyle(QStyleFactory.create(styleName))

    # 生成并显示主窗口
    main_window = MainWindow()
    main_window.show()

    # 进入主程序循环直到退出
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()