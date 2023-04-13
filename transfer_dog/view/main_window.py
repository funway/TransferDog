#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import os, sys, logging

from playhouse.shortcuts import model_to_dict
from PySide6.QtWidgets import QMainWindow, QDialog, QAbstractItemView, QLineEdit
from PySide6.QtGui import QStandardItemModel, QStandardItem

from transfer_dog.model import Task
from transfer_dog.ui.ui_main_window import Ui_MainWindow
from transfer_dog.view.dialog_task_edit import DialogTaskEdit
from transfer_dog.view.task_info import *


class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)
        
        # 定义成员变量
        self.tree_model = QStandardItemModel()

        # 调用父类 Ui_MainWindow 的函数装载 UI
        self.setupUi(self)
        
        # 绑定信号-槽
        self.actionNewTask.triggered.connect(lambda: self.show_dialog_task_edit(None))

        self.update_UI()
        pass

    def update_UI(self):
        """执行一些无法在 setupUi() 中完成的界面更新
        """

        # 获取有效任务
        tasks = [task for task in Task.select()]
        for task in tasks:
            self.logger.debug('task: %s', task)

        # 获取任务组
        groups = list(set([task.group_name for task in tasks]))
        groups.sort()   # sort() 并不能很好地处理中文排序，因为它只是按照字符编码进行排序，而中文的编码顺序与拼音顺序无关。
        self.logger.debug('There are %s taskgroups: %s', len(groups), groups)

        # 设置 model
        root_item = self.tree_model.invisibleRootItem()
        
        # 添加 model 子节点
        group_index = {}
        # 添加一级节点 任务组
        for group in groups:
            # 添加一级节点 任务组
            gp_item = QStandardItem(group)
            root_item.appendRow(gp_item)
            group_index[group] = root_item.rowCount() - 1
            pass
        # 添加二级节点 任务
        for task in tasks:
            tk_item = TaskInfoItem(task.task_name)
            root_item.child(group_index[task.group_name]).appendRow(tk_item)
            # 将每个 tk_item.widget 的 parent 设置为当前 QTreeView
            tk_item.widget.setParent(self.treeView.viewport())
            tk_item.widget.installEventFilter(self.treeView)
            pass

        # 定义 ProxyModel
        self.proxy_model = TaskSearchProxyModel()
        self.proxy_model.setSourceModel(self.tree_model)

        # 给 QTreeView 设置数据
        self.treeView.setModel(self.proxy_model)
        
        # 给 QTreeView 设置自定义的 ItemDelegate
        delegate = TaskInfoDelegate()
        self.treeView.setItemDelegate(delegate)

        # 关联 QTreeView 的 节点展开、收缩 事件
        self.treeView.expanded.connect(self._tree_view_item_expanded)
        self.treeView.collapsed.connect(self._tree_view_item_collapsed)
        self.treeView.clicked.connect(self._tree_view_item_clicked)

        # 给 QTreeView 设置其他参数
        self.treeView.setHeaderHidden(True)
        # self.treeView.setIndentation(0)
        # self.treeView.setRootIsDecorated(False)
        self.treeView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeView.expandAll()

        # 设置搜索栏
        self.lineEdit.addAction(QIcon(str(RESOURCE_PATH / 'img/search-line.png')), QLineEdit.ActionPosition.LeadingPosition)
        self.lineEdit.textChanged.connect(self._search_text_changed)
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
    
    def _tree_view_item_collapsed(self, idx):
        self.logger.debug('QTreeView collpase at node [%s]', idx.data())
        # 隐藏其下的任务子节点
        for row in range(idx.model().rowCount(idx)):
            child_idx = idx.model().index(row, 0, idx)
            child_item = self.tree_model.itemFromIndex(idx.model().mapToSource(child_idx))
            child_item.widget.hide()
            pass
        pass

    def _tree_view_item_expanded(self, idx):
        self.logger.debug('QTreeView expand at node [%s]', idx.data())
        # 显示其下的任务子节点
        for row in range(idx.model().rowCount(idx)):
            child_idx = idx.model().index(row, 0, idx)
            tk_widget = child_idx.data(role=QtCore.Qt.ItemDataRole.UserRole)
            tk_widget.show()
            pass
        pass

    def _tree_view_item_clicked(self, idx):
        self.logger.debug('idx clicked! [%s]', idx.data())
        
        # 获取当前被点击的 QStandardItem
        item = self.tree_model.itemFromIndex(idx.model().mapToSource(idx))
        # self.logger.debug(item.data(role=QtCore.Qt.ItemDataRole.DisplayRole))
        pass

    def _search_text_changed(self, text):
        self.logger.debug('Search text changed: %s', text)
        self.proxy_model.setFilterRegularExpression(text)
        self.treeView.expandAll()
        pass

    def __del__(self):
        self.logger.debug('Delete a %s instance', self.__class__.__name__)
        pass