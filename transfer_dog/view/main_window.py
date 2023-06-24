#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import os, sys, logging, configparser
from datetime import datetime
from ast import literal_eval

import psutil
from playhouse.shortcuts import model_to_dict
from PySide6.QtWidgets import QMainWindow, QDialog, QAbstractItemView, QLineEdit, QMessageBox, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFontMetrics, QStandardItemModel, QStandardItem, QDesktopServices
from PySide6.QtCore import Qt
from peewee import SqliteDatabase

from transfer_dog.transfer_dog import TransferDog
from transfer_dog.ui.ui_main_window import Ui_MainWindow
from transfer_dog.view.dialog_task_edit import DialogTaskEdit
from transfer_dog.view.task_treeview import *
from transfer_dog.utility import helper
from transfer_worker.model import Task
from transfer_worker.model import Processed


class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)
        
        # 定义成员变量
        self.doggy = TransferDog()
        self.source_model = TaskItemModel()
        self.proxy_model = TaskSearchProxyModel()
        self.tb_processed_current_uuid = None

        self.lab_uptime = QLabel(parent=self)
        self.lab_uptime.setObjectName('lab_uptime')
        
        # 调用父类 Ui_MainWindow 的函数装载 UI
        self.setupUi(self)
        
        # 绑定信号-槽
        self.actionNewTask.triggered.connect(lambda: self.show_dialog_task_edit(None, 'New Task'))
        self.actionEditTask.triggered.connect(self._action_edit_task)
        self.actionDeleteTask.triggered.connect(self._action_delete_task)
        self.actionCopyTask.triggered.connect(self._action_copy_task)
        self.actionStartTask.triggered.connect(self._action_start_task)
        self.actionStopTask.triggered.connect(self._action_kill_task)
        self.actionOpenSource.triggered.connect(self._action_open_source)
        self.actionOpenDest.triggered.connect(self._action_open_dest)
        self.actionOpenLogFile.triggered.connect(self._action_open_log_file)
        self.actionOpenProcessedDB.triggered.connect(self._action_open_processed_db)
        self.actionHelp.triggered.connect(self._action_help)

        self.update_UI()
        
        # 启动一个 1000 ms 的定时器，定时自动调用 self.timerEvent() 方法
        self.timer_one_second = self.startTimer(1000)
        pass

    def timerEvent(self, event: QtCore.QTimerEvent):
        self.logger.debug('定时器事件 (timer id: %s)', event.timerId())

        if event.timerId() == self.timer_one_second:
            # 需要每秒钟触发的定时事件
            # 1. 刷新状态栏显示的运行时间
            self._update_uptime()
            # 2. 刷新 table 中的 processed 记录
            self._tb_process_load(self.tb_processed_current_uuid)

        super().timerEvent(event)
        pass

    def test_func(self):
        self.logger.info('测试测试')
        self.logger.info('viewport rect: %s', self.treeView.viewport().rect())
        # for (uuid, item) in self.source_model.dict_task_item.items():
        #     idx = self.proxy_model.indexFromItem(item)
        #     # self.logger.info('item (%s) is visible? %s', idx.data(), self.treeView.isRowHidden(0, idx.parent()))
            
        #     intersect = self.treeView.visualRect(idx).intersects(self.treeView.viewport().rect())
        #     self.logger.info('[%s] visual rect: %s. intersect: %s, isvalid: %s', idx.data(), self.treeView.visualRect(idx), intersect, idx.isValid())
        #     self.logger.info('above: %s, bellow: %s', self.treeView.indexAbove(idx).data(), self.treeView.indexBelow(idx).data())

        #     pass
        
        # 判断左上节点，右下节点
        idx_topleft = self.treeView.indexAt(self.treeView.viewport().rect().topLeft())
        idx_bottomright = self.treeView.indexAt(self.treeView.viewport().rect().bottomRight())
        self.logger.info('左上节点: %s, 右下节点: %s', idx_topleft.data(), idx_bottomright.data())
        self.logger.info('上上: %s, 下下: %s', self.treeView.indexAbove(idx_topleft).isValid(), self.treeView.indexBelow(idx_bottomright).isValid())

        self._ensure_outrange_taskinfo_hidden()
        pass

    def add_task(self, task: Task):
        """新增 task
        1. 将 task 加入到 TransferDog 单例中，
        包括 task 字典, task_satatus 字典(新建 status), task_widget 字典(新建 widget)
        并设置 widget 的父节点为 treeview

        2. 在 TaskInfoModel 中新增 item

        Args:
            task (Task): _description_
        """
        # 1. 将 task 加入到 doggy 的 task 字典
        if task.uuid in self.doggy.dict_tasks:
            self.logger.warning('task[%s] 已存在于 TransferDog 单例中！', task.uuid)
        else:
            self.doggy.dict_tasks[task.uuid] = task
            self.doggy.dict_task_statuses[task.uuid] = TaskStatus(schedule=task.schedule, enabled=task.enabled)
            widget = TaskWidget(task.task_name)
            widget.setParent(self.treeView.viewport())
            widget.installEventFilter(self.treeView)
            self.doggy.dict_task_widgets[task.uuid] = widget
            widget.hide()

        # 2. 将 task 加入到 source_model 中
        self.source_model.add_task(task)

        # 3. 在 treeview 中展开 item 对应的任务组
        # item = self.source_model.find_task(task.uuid)
        # idx = self.proxy_model.indexFromItem(item)
        # self.treeView.expand(idx.parent())
        pass
    
    def add_tasks(self, tasks):
        for task in tasks:
            self.add_task(task)
        pass

    def remove_task(self, task: Task):
        """从 TransferDog 的字典中删除 task
        包括 tasks 字典， statuses 字典(杀死在运行的任务进程), widgets 字典(并销毁 widget 实例), visible_tasks 集合
        但不包括从数据库中删除 task

        Args:
            task (Task): _description_
        """
        # 1 从 model 中删除 item
        self.source_model.remove_task(task.uuid)
                
        # 2 从 doggy 的 tasks 字典中删除 task
        task = self.doggy.dict_tasks.pop(task.uuid)
        
        # 3 从 doggy 的 task_widgets 字典中删除 task 对应的 widget
        widget = self.doggy.dict_task_widgets.pop(task.uuid)
        widget.setParent(None)

        # 4 从 doggy 的 task_statused 字典中删除 task 对应的状态，并杀死正在运行的任务子进程
        status = self.doggy.dict_task_statuses.pop(task.uuid, None)
        if status is not None and status.process is not None and status.process.is_running():
            status.process.kill()

        # 5 从 doggy 的 set_visible_task 集合中删除
        self.doggy.set_visible_tasks.discard(task.uuid)
        pass

    def update_UI(self):
        """执行一些无法在 setupUi() 中完成的界面更新
        """
        # 从数据库中读取所有 task
        tasks = [task for task in Task.select()]
        self.add_tasks(tasks)

        # 设置 ProxyModel
        self.proxy_model.setSourceModel(self.source_model)

        # 给 QTreeView 设置数据
        self.treeView.setModel(self.proxy_model)
        self.treeView.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        
        # 给 QTreeView 设置自定义的 ItemDelegate
        delegate = TaskItemDelegate()
        self.treeView.setItemDelegate(delegate)

        # 关联 QTreeView 的 节点展开、收缩 事件
        self.treeView.expanded.connect(self._treeview_item_expanded)
        self.treeView.collapsed.connect(self._treeview_item_collapsed)
        self.treeView.clicked.connect(self._treeview_clicked)
        self.treeView.doubleClicked.connect(self._treeview_double_clicked)
        self.treeView.verticalScrollBar().valueChanged.connect(self._on_v_scroll_changed)

        # 给 QTreeView 设置其他参数
        self.treeView.setHeaderHidden(True)
        # self.treeView.setIndentation(0)
        # self.treeView.setRootIsDecorated(False)
        self.treeView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeView.expandAll()

        # 设置搜索栏
        self.lineEdit.addAction(QIcon(str(RESOURCE_PATH / 'img/search-line.png')), QLineEdit.ActionPosition.LeadingPosition)
        self.lineEdit.textChanged.connect(self._search_text_changed)

        # 设置底部状态栏
        self.statusBar.addWidget(self.lab_uptime)
        self.statusBar.addPermanentWidget(QLabel('© %s funway' % datetime.now().strftime('%Y')))

        # 设置 QSplitter 初始比例
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

        # 设置 table 的基本属性
        self.tb_processed.setColumnCount(3)
        self.tb_processed.setHorizontalHeaderLabels(['id', 'file', 'processed_at'])
        self.tb_processed.verticalHeader().setVisible(False)
        self.tb_processed.setColumnWidth(0, 50)
        self.tb_processed.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tb_processed.setColumnWidth(2, 150)

        self._update_uptime()

        pass

    def get_selected_task_item(self):
        """获取用户当前选中的任务列表中的任务项, 如果无选中则返回 None 并在状态栏显示 message

        Returns:
            TaskItem / None: _description_
        """
        ss = self.treeView.selectedIndexes()
        if len(ss) == 0:
            self.logger.debug('用户没有选中任何节点')
            self.statusBar.showMessage('未选中任务', timeout=3000)
            return None
        
        idx = ss[0]
        item = idx.model().itemFromIndex(idx)
        if type(item) is TaskItem:
            self.logger.debug('用户选中的是任务节点 [%s]', idx.data())
            return item
        else:
            self.logger.debug('用户选中的不是任务节点')
            self.statusBar.showMessage('未选中任务', timeout=3000)
            return None

    def _action_delete_task(self):
        item = self.get_selected_task_item()
        if item is not None:
            self.logger.debug('用户选中删除任务节点 [%s]', item.data(role=QtCore.Qt.ItemDataRole.DisplayRole))
            reply = QMessageBox.question(self, 'Delete Task', 'You sure to delete task [{0}]?'.format(item.data(role=QtCore.Qt.ItemDataRole.DisplayRole)),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.Yes:
                self.logger.debug('用户选择了 Yes')

                task = self.doggy.dict_tasks[item.task_uuid]
                
                self.remove_task(task)
                
                # 从数据库中删除该实例
                task.delete_instance()
            else:
                self.logger.debug('用户选择了 No')
        pass

    def _action_edit_task(self):
        item = self.get_selected_task_item()
        if item is not None:
            self.logger.debug('用户选中编辑任务节点 [%s]', item.data(role=QtCore.Qt.ItemDataRole.DisplayRole))
            self.show_dialog_task_edit(task=self.doggy.dict_tasks[item.task_uuid], window_title='Edit Task')
        pass
    
    def _action_copy_task(self):
        item = self.get_selected_task_item()
        if item is not None:
            self.logger.debug('用户选中复制任务节点 [%s]', item.data(role=QtCore.Qt.ItemDataRole.DisplayRole))
            src_task = self.doggy.dict_tasks[item.task_uuid]
            copy_task = src_task.copy()
            self.show_dialog_task_edit(task=copy_task, window_title='New Task (copy)')
        pass

    def _action_start_task(self):
        item = self.get_selected_task_item()
        if item is not None:
            self.logger.debug('用户选中启动任务 [%s]', item.data(role=QtCore.Qt.ItemDataRole.DisplayRole))
            self.doggy.start_task(item.task_uuid)
        pass

    def _action_kill_task(self):
        item = self.get_selected_task_item()
        if item is not None:
            self.logger.debug('用户选中杀死任务 [%s]', item.data(role=QtCore.Qt.ItemDataRole.DisplayRole))
            self.doggy.kill_task(item.task_uuid)
        pass

    def _action_open_source(self):
        item = self.get_selected_task_item()
        if item is not None:
            task = self.doggy.dict_tasks[item.task_uuid]
            
            url = helper.rebuild_standard_url(task.source_url, task.source_username, task.source_password)
            
            # QDesktopServices.openUrl('file:///Users/funway/project/')
            if not QDesktopServices.openUrl(url):
                self.statusBar.showMessage('无法打开源目录', timeout=3000)
        pass
    
    def _action_open_dest(self):
        item = self.get_selected_task_item()
        if item is not None:
            task = self.doggy.dict_tasks[item.task_uuid]
            
            url = helper.rebuild_standard_url(task.dest_url, task.dest_username, task.dest_password)
            
            if not QDesktopServices.openUrl(url):
                self.statusBar.showMessage('无法打开目标目录', timeout=3000)
        pass

    def _action_open_log_file(self):
        item = self.get_selected_task_item()
        if item is not None:
            self.logger.debug('用户选中查看任务日志 [%s]', item.data(role=QtCore.Qt.ItemDataRole.DisplayRole))
            worker_log_file = None
            worker_log_config = configparser.ConfigParser(defaults={'task_uuid': item.task_uuid})
            worker_log_config.read(WORKER_LOGGIN_CONFIG, encoding='UTF8')
            worker_log_config_args = worker_log_config.get('handler_fileHandler', 'args', fallback=None)
            if worker_log_config_args is not None:
                worker_log_file_path = Path(literal_eval(worker_log_config_args)[0])
                if not worker_log_file_path.is_absolute():
                    worker_log_file_path = PROJECT_PATH.joinpath(worker_log_file_path)
                if worker_log_file_path.exists():
                    worker_log_file = str(worker_log_file_path)
            
            self.logger.debug('任务日志: %s', worker_log_file)
            if worker_log_file is None:
                self.statusBar.showMessage('未找到日志文件', timeout=3000)
            else:
                QDesktopServices.openUrl('file://%s' % worker_log_file)
            
        pass
    
    def _action_open_processed_db(self):
        item = self.get_selected_task_item()
        if item is not None:
            processed_db = PROCESSED_PATH.joinpath(item.task_uuid + '.db')
            if processed_db.exists():
                QDesktopServices.openUrl('file://%s' % processed_db)
            else:
                self.statusBar.showMessage('未找到 processed db', timeout=3000)
        pass

    def _action_help(self):
        QDesktopServices.openUrl('fiile://%s' % PROJECT_PATH.joinpath('README.md'))
        pass

    def show_dialog_task_edit(self, task:Task=None, window_title=None):
        self.logger.debug('show dialog_task_edit with task: %s', task)
        
        dialog = DialogTaskEdit(task=task)
        dialog.setWindowTitle(window_title)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.logger.debug("dialog save clicked!")
            task = dialog.retrieve_task()
            self.logger.debug('retrieve task: %s', model_to_dict(task))
            self.logger.debug('dirty fields: %s', task.dirty_fields)
            
            try:
                if task.uuid not in self.doggy.dict_tasks:
                    self.logger.debug('保存新建的 task. %s', task)
                    task.save()
                    self.add_task(task)
                    pass
                elif task.is_dirty():
                    self.logger.debug('保存修改的 task. %s', task)
                    
                    for dirty_field in task.dirty_fields:
                        if Task.group_name is dirty_field:
                            self.logger.debug('修改了 task 的任务组，需要对任务列表进行重排')
                            self.source_model.remove_task(task.uuid)
                            self.source_model.add_task(task)
                            
                            item = self.source_model.find_task(task.uuid)
                            idx = self.proxy_model.indexFromItem(item)
                            self.treeView.expand(idx.parent())
                            self.treeView.selectionModel().select(idx,
                                QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)
                            break

                    item = self.source_model.find_task(task.uuid)
                    item.setData(task.task_name, role=QtCore.Qt.ItemDataRole.DisplayRole)
                    self.doggy.dict_task_widgets[task.uuid].label_title.setText(task.task_name)
                    task.save()
                    pass
                
                # 不管增加节点还是变更任务组，都有可能导致原来可视区域的节点变化，所以需要确保原来可见现在不可见的节点被安全的 hide
                self._ensure_outrange_taskinfo_hidden()
            except Exception as e:
                self.logger.exception('保存任务失败！')
                pass
        else:
            self.logger.debug("dialog cancel clicked")
        pass
    
    def _treeview_item_collapsed(self, idx):
        self.logger.debug('QTreeView collpase at node [%s]', idx.data())
        # 隐藏其下的任务子节点
        for row in range(idx.model().rowCount(idx)):
            child_idx = idx.model().index(row, 0, idx)
            child_item = idx.model().itemFromIndex(child_idx)
            self.doggy.hide(child_item.task_uuid)
            pass
        pass

    def _treeview_item_expanded(self, idx):
        self.logger.debug('QTreeView expand at node [%s]', idx.data())

        self._ensure_outrange_taskinfo_hidden()
        pass

    def _ensure_outrange_taskinfo_hidden(self):
        for uuid in self.doggy.set_visible_tasks.copy():
            item = self.source_model.find_task(uuid)
            index = self.proxy_model.indexFromItem(item)
            self.logger.debug('(%s) 节点原来可见', index.data())

            intersect = self.treeView.visualRect(index).intersects(self.treeView.viewport().rect())
            if not intersect:
                self.logger.debug('(%s) 节点不再可见', index.data())
                self.doggy.hide(uuid)
        pass

    def _treeview_clicked(self, idx):
        self.logger.debug('idx clicked. [%s]', idx.data())
        
        # 获取当前被点击的 QStandardItem
        item = idx.model().itemFromIndex(idx)
        if type(item) is TaskItem:
            self.logger.debug('用户单击任务节点 [%s]', idx.data())
            
            self._tb_process_load(uuid=item.task_uuid)
        else:
            self.logger.debug('用户单击的不是任务节点')
        pass

    def _treeview_double_clicked(self, idx):
        self.logger.debug('idx double clicked. [%s]', idx.data())
        item = idx.model().itemFromIndex(idx)
        if type(item) is TaskItem:
            self.logger.debug('用户双击任务节点 [%s]', idx.data())
            self.show_dialog_task_edit(task=self.doggy.dict_tasks[item.task_uuid], window_title='Edit Task')
        else:
            self.logger.debug('用户双击的不是任务节点')
        pass

    def _search_text_changed(self, text):
        self.logger.debug('Search text changed: %s', text)
        self.proxy_model.setFilterRegularExpression(text)
        self.treeView.expandAll()
        pass

    def _on_v_scroll_changed(self, value):
        self.logger.debug('V scroll bar value changed to: %s', value)
        self._ensure_outrange_taskinfo_hidden()
        pass

    def _tb_process_load(self, uuid):
        """加载并显示指定任务的 processed 文件

        Args:
            uuid (_type_): 要显示的任务的 uuid
        """

        # 如果当前已显示的 uuid 与指定的 uuid 参数不一致，则清空 tableview
        if self.tb_processed_current_uuid != uuid:
            self.logger.debug('table_processed 切换要显示的任务')
            # self.tb_processed.clear()
            self.tb_processed.setRowCount(0)
            self.tb_processed_current_uuid = uuid
            pass
        
        if uuid is None:
            return 
        
        self.logger.debug('加载任务[%s]的 processed 记录', uuid)

        # 1 判断 processed.db 文件是否存在
        processed_db_file = PROCESSED_PATH.joinpath(uuid + '.db')
        if not processed_db_file.exists():
            self.logger.debug('processed 文件不存在. 返回')
            return 

        # 2 获取当前已显示的最大 id
        max_id = 0 if self.tb_processed.item(0, 0) is None else str(self.tb_processed.item(0, 0).text())
        self.logger.debug('已加载的最大 id: %s', max_id)

        processed_db = SqliteDatabase(str(processed_db_file))
        processed_db.bind([Processed, ])
        processed_db.create_tables([Processed], safe=True)
        
        # 3 查询更新的 processed 记录
        if max_id == 0:
            query = (Processed
                     .select()
                     .order_by(Processed.id.desc())
                     .limit(TABLE_MAX_ROWS)
                     )
        else:
            query = (Processed
                    .select()
                    .where(Processed.id > max_id)
                    .order_by(Processed.id.asc())
                    .limit(TABLE_MAX_ROWS)
                    )
        
        for p in query:
            self.logger.debug(p)
            new_row = self.tb_processed.rowCount() if max_id == 0 else 0
            self.tb_processed.insertRow(new_row)
            self.tb_processed.setItem(new_row, 0, QTableWidgetItem(str(p.id)))
            self.tb_processed.setItem(new_row, 1, QTableWidgetItem(p.source))
            self.tb_processed.setItem(new_row, 2, QTableWidgetItem(p.processed_at.strftime(TIME_FORMAT)))

        pass

    def _update_uptime(self):
        start_time = datetime.fromtimestamp(psutil.Process().create_time())
        uptime = datetime.now() - start_time
        self.logger.debug('uptime: %s', uptime)
        
        # use <pre> tag to keep space on (or else HTML will shrink extra spaces to one space)
        # use <code> tag to make sure the widget show the string with monospace font in all platform
        self.lab_uptime.setText('<pre><code>up time: {} days {:2} hours {:2} minutes {:2} seconds</code></pre>'.format(
            uptime.days, uptime.seconds//3600, uptime.seconds%3600//60, uptime.seconds%60))
        pass
    
    
    def __del__(self):
        self.logger.debug('Delete a %s instance', self.__class__.__name__)
        pass