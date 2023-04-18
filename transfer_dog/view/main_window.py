#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import os, sys, logging

from playhouse.shortcuts import model_to_dict
from PySide6.QtWidgets import QMainWindow, QDialog, QAbstractItemView, QLineEdit
from PySide6.QtGui import QStandardItemModel, QStandardItem

from transfer_dog.transfer_dog import TransferDog
from transfer_dog.ui.ui_main_window import Ui_MainWindow
from transfer_dog.view.dialog_task_edit import DialogTaskEdit
from transfer_dog.view.task_info import *
from transfer_worker.model import Task


class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)
        
        # 定义成员变量
        self.doggy = TransferDog()
        self.source_model = TaskInfoItemModel()
        self.proxy_model = TaskSearchProxyModel()

        # 调用父类 Ui_MainWindow 的函数装载 UI
        self.setupUi(self)
        
        # 绑定信号-槽
        self.actionNewTask.triggered.connect(lambda: self.show_dialog_task_edit(None))
        self.actionEditTask.triggered.connect(self._action_edit_task)
        self.actionDeleteTask.triggered.connect(self._action_delete_task)
        self.actionCopyTask.triggered.connect(self._action_copy_task)
        self.actionTest.triggered.connect(self.test_func)

        self.update_UI()
        pass

    def test_func(self):
        self.logger.info('测试测试')
        pass

    def add_task(self, task: Task):
        """新增 task：将 task 加入到 TransferDog 单例中，加入到 TaskInfoModel 中，并给其对应的 widget 设置父节点。

        Args:
            task (Task): _description_
        """
        # 1. 将 task 加入到 doggy 的 task 字典
        if task.uuid in self.doggy.tasks:
            self.logger.warning('task[%s] 已存在于 TransferDog 单例中！', task.uuid)
        else:
            self.doggy.tasks[task.uuid] = task

        # 2. 将 task 加入到 source_model 中
        self.source_model.add_task(task)

        # 3. 给 TaskInfoItem.widget 设置父节点，绑定到 treeView 中
        item = self.source_model.find_task(task.uuid)
        item.widget.setParent(self.treeView.viewport())
        item.widget.show()

        # 4. 在 treeview 中展开 item 对应的任务组
        idx = self.proxy_model.indexFromItem(item)
        self.treeView.expand(idx.parent())
        pass
    
    def update_UI(self):
        """执行一些无法在 setupUi() 中完成的界面更新
        """
        # 设置 Model
        self.source_model.add_tasks(self.doggy.tasks.values())

        # 设置 ProxyModel
        self.proxy_model.setSourceModel(self.source_model)

        # 给 QTreeView 设置数据
        self.treeView.setModel(self.proxy_model)
        self.treeView.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        
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

    def _action_delete_task(self):
        ss = self.treeView.selectedIndexes()
        if len(ss) == 0:
            self.logger.debug('用户没有选中任何节点')
            return
        idx = ss[0]
        item = idx.model().itemFromIndex(idx)
        if type(item) is TaskInfoItem:
            self.logger.debug('用户选中删除任务节点 [%s]', idx.data())
            self.source_model.remove_task(item.task_uuid)
            task = self.doggy.tasks.pop(item.task_uuid)
            task.delete_instance()
        else:
            self.logger.debug('用户选中的不是任务节点')
        pass

    def _action_edit_task(self):
        ss = self.treeView.selectedIndexes()
        if len(ss) == 0:
            self.logger.debug('用户没有选中任何节点')
            return
        
        idx = ss[0]
        item = idx.model().itemFromIndex(idx)
        if type(item) is TaskInfoItem:
            self.logger.debug('用户选中编辑任务节点 [%s]', idx.data())
            self.show_dialog_task_edit(task=self.doggy.tasks[item.task_uuid])
        else:
            self.logger.debug('用户选中的不是任务节点')
        pass
    
    def _action_copy_task(self):
        ss = self.treeView.selectedIndexes()
        if len(ss) == 0:
            self.logger.debug('用户没有选中任何节点')
            return
        idx = ss[0]
        item = idx.model().itemFromIndex(idx)
        if type(item) is TaskInfoItem:
            self.logger.info('用户选中复制任务节点 [%s]', idx.data())
            src_task = self.doggy.tasks[item.task_uuid]
            copy_task = src_task.copy()
            copy_task.save()
            self.add_task(copy_task)
        else:
            self.logger.debug('用户选中的不是任务节点')
        pass
        pass

    def show_dialog_task_edit(self, task:Task=None):
        self.logger.debug('show dialog_task_edit with task: %s', task)
        
        dialog = DialogTaskEdit(task=task)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.logger.debug("dialog save clicked!")
            task = dialog.retrieve_task()
            self.logger.debug('retrieve task: %s', model_to_dict(task))
            self.logger.debug('dirty fields: %s', task.dirty_fields)
            
            try:
                if task.uuid not in self.doggy.tasks:
                    self.logger.debug('保存新建的 task. %s', task)
                    self.add_task(task)
                    task.save()
                    pass
                elif task.is_dirty():
                    self.logger.debug('保存修改的 task. %s', task)
                    item = self.source_model.find_task(task.uuid)
                    
                    for dirty_field in task.dirty_fields:
                        if Task.group_name is dirty_field:
                            self.logger.debug('修改了 task 的任务组，需要对任务列表进行重排')
                            self.source_model.remove_task(task.uuid)
                            self.source_model.add_task(task)
                            
                            item = self.source_model.find_task(task.uuid)
                            item.widget.setParent(self.treeView.viewport())
                            item.widget.show()
                            
                            idx = self.proxy_model.indexFromItem(item)
                            self.treeView.expand(idx.parent())
                            self.treeView.selectionModel().select(idx,
                                QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)
                            break
                    
                    item.widget.label_title.setText(task.task_name)
                    task.save()
                    pass
            except Exception as e:
                self.logger.exception('保存任务失败！')
                pass
        else:
            self.logger.debug("dialog cancel clicked")
        pass
    
    def _tree_view_item_collapsed(self, idx):
        self.logger.debug('QTreeView collpase at node [%s]', idx.data())
        # 隐藏其下的任务子节点
        for row in range(idx.model().rowCount(idx)):
            child_idx = idx.model().index(row, 0, idx)
            child_item = idx.model().itemFromIndex(child_idx)
            child_item.widget.hide()
            pass
        pass

    def _tree_view_item_expanded(self, idx):
        self.logger.debug('QTreeView expand at node [%s]', idx.data())
        # 显示其下的任务子节点
        for row in range(idx.model().rowCount(idx)):
            child_idx = idx.model().index(row, 0, idx)
            child_item = idx.model().itemFromIndex(child_idx)
            child_item.widget.show()
            # tk_widget = child_idx.data(role=QtCore.Qt.ItemDataRole.UserRole)
            # tk_widget.show()
            pass
        pass

    def _tree_view_item_clicked(self, idx):
        self.logger.debug('idx clicked! [%s]', idx.data())
        
        # 获取当前被点击的 QStandardItem
        item = idx.model().itemFromIndex(idx)
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