#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import os, sys, sqlite3, logging, logging.config
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from ui.ui_main_window import Ui_MainWindow
from task_edit_dialog import TaskEditDialog

from utilities.constants import *

class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance' % self.__class__.__name__)
        
        # 定义成员变量
        self.config_db_conn = None
        self.config_db_cursor = None
        self.load_config()

        # 装载 UI
        self.setupUi(self)
        
        # 绑定信号-槽
        self.actionNewTask.triggered.connect(self.slot_show_edit_task_dialog)

        pass

    def load_config(self, config_db = CONFIG_DB):
        os.makedirs(os.path.dirname(config_db), exist_ok=True)
        self.config_db_conn = sqlite3.connect(config_db)
        self.config_db_cursor = self.config_db_conn.cursor()

        try:
            res = self.config_db_cursor.execute('SELECT * FROM {tb}'.format(tb=CONFIG_TABLE_TASKS))
            pass
        except Exception as e:
            self.logger.debug("任务表不存在，准备新建任务表")
            sql_create = """CREATE TABLE {tb}(
                name TEXT NOT NULL, 
                enabled INTEGER NOT NULL CHECK(enabled IN (0, 1))
                );
            """.format(tb=CONFIG_TABLE_TASKS)

            self.config_db_cursor.execute(sql_create)
            pass
        else:
            pass
        finally:
            pass

        pass

    def slot_show_edit_task_dialog(self):
        
        dialog = TaskEditDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.logger.debug("dialog save clicked!")
            self.add_task(dialog)
        else:
            self.logger.debug("dialog cancel clicked")
        pass

    def add_task(self, dialog:TaskEditDialog):
        self.logger.debug("task name: %s" % dialog.leditTaskName.text())

        sql_insert = """INSERT INTO {tb} VALUES (?, ?)
        """.format(tb=CONFIG_TABLE_TASKS)
        
        self.config_db_cursor.execute(sql_insert, (dialog.leditTaskName.text(), False))
        self.config_db_conn.commit()
        pass

    def __del__(self):
        if self.config_db_cursor is not None:
            self.config_db_cursor.close()
        if self.config_db_conn is not None:
            self.config_db_conn.close()
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
    with open(BASE_PATH + '/ui/resources/stylesheets/default.qss', 'r') as qss_file:
        qss = qss_file.read()
        app.setStyleSheet(qss)

    # 生成并显示主窗口
    main_window = MainWindow()
    main_window.show()

    # 进入主程序循环直到退出
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()