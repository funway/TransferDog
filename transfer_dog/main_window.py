#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import os, sys, logging

from playhouse.shortcuts import model_to_dict
from PySide6.QtWidgets import QMainWindow, QDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem

from transfer_dog.model import Task
from transfer_dog.ui.ui_main_window import Ui_MainWindow
from transfer_dog.dialog_task_edit import DialogTaskEdit


class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)
        
        # 定义成员变量
        self.taskModel = QStandardItemModel()

        # 调用父类 Ui_MainWindow 的函数装载 UI
        self.setupUi(self)
        
        # 绑定信号-槽
        self.actionNewTask.triggered.connect(lambda: self.show_dialog_task_edit(None))

        self.update_UI()
        pass

    def update_UI(self):
        """执行一些无法在 setupUi() 中完成的界面更新
        """
        # self.treeView.setHeaderHidden(True)
        # self.treeview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        for task in Task.select():
            self.logger.debug('task: %s', task)
        
        groups = [task.group_name for task in Task.select()]
        self.logger.debug(groups)

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
        self.logger.debug('Delete a %s instance', self.__class__.__name__)
        pass