#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/01/11 19:56:02

if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append( str(Path(__file__).parent.parent.parent) )
    pass


import logging, re

from croniter import croniter
from peewee import fn
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QIntValidator
from PySide6.QtWidgets import QDialog

from transfer_dog.ui.ui_dialog_task_edit import Ui_Dialog
from transfer_dog.view.server_widget import ServerWidget
from transfer_dog.view.dialog_regular_express import DialogRegularExpress
from transfer_worker.model.task import Task
from transfer_dog.utility.constants import *


task_valid_time_options = {
    -1: 'All Time',
    10: '10 Minutes',
    30: '30 Minutes',
    60: '1 Hour',
    180: '3 Hours',
    720: '12 Hours',
    1440: '24 Hours'}


class DialogTaskEdit(QDialog, Ui_Dialog):
    """docstring for DialogTaskEdit."""

    def __init__(self, task:Task=None):
        super(DialogTaskEdit, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        # 定义成员变量
        if task is None:
            self._task = Task()
            self.logger.debug('新建任务. [%s] %s', self._task.uuid, self._task)
        else:
            self._task = task
            self.logger.debug('修改任务. [%s]', self._task.uuid)

        # 装载 UI
        self.setupUi(self)
        self.sw_source = ServerWidget(self._task.source_url, self._task.source_username, self._task.source_password)
        self.sw_dest = ServerWidget(self._task.dest_url, self._task.dest_username, self._task.dest_password)

        # 绑定 信号-槽
        self.pb_regex_test.clicked.connect(self.show_regex_test_dialog)

        # 根据 _task 更新 UI
        self.update_UI()
        pass

    def update_UI(self):
        """Update dialog UI according to the self._task. Do some UI updating that cannot be done in setupUI().
        """        
        task = self._task

        #   初始化任务分组下拉框
        groups = [row['group_name'] for row in Task.select( fn.Distinct(Task.group_name) ).dicts()]
        groups.sort()
        self.comb_task_group.addItems(groups)

        # update general group
        self.le_task_name.setText(task.task_name)
        self.comb_task_group.setCurrentText(task.group_name)
        self.le_task_schedule.setText(task.schedule)
        self.chkb_task_enabled.setChecked(task.enabled)
        self.le_timeout.setText(str(task.timeout))
        self.le_timeout.setValidator(QIntValidator(0, 999999999))
        
        # update source group
        self.gbox_source.layout().addWidget(self.sw_source)

        # update filter group
        #   文件名过滤
        self.le_filter_filename.setText(task.filter_filename)
        #   子目录递归
        self.spinBox_subdir_recursion.setValue(task.subdir_recursion)
        #   有效时间过滤
        for key, text in task_valid_time_options.items():
            self.comb_filter_valid_time.addItem(text, key)
        try:
            self.comb_filter_valid_time.setCurrentText(task_valid_time_options[self._task.filter_valid_time])
        except Exception as e:
            logging.exception('task.filter_valid_time 异常！无法找到对应的选项')
            self.comb_filter_valid_time.setCurrentIndex(0)
        #   中间件
        self.comb_middleware.addItem('None', None)
        middlewares = [fname.name for fname in MIDDLEWARE_PATH.glob('*.py')]
        middlewares.sort()
        for mw in middlewares:
            self.comb_middleware.addItem(mw, mw)
        self.comb_middleware.setCurrentIndex(self.comb_middleware.findText('None' if task.middleware is None else task.middleware))
        self.le_middleware_arg.setText(task.middleware_arg)
        #   临时后缀
        self.le_suffix.setText(task.suffix)
        #   处理历史
        self.le_processed_reserve.setText(str(task.processed_reserve_time))
        self.le_processed_reserve.setValidator(QIntValidator(0, 999999999))
        #   删除源文件
        self.chkb_delete_source.setChecked(task.delete_source)

        # update destination group
        self.gbox_dest.layout().addWidget(self.sw_dest)

        pass

    def retrieve_task(self) -> Task:
        """从对话框实例中获取 Task 实例。

        Returns:
            Task: 返回 self._task。在返回之前，需要先从对话框面板获取更新数据。
        """

        # general group
        if self._task.task_name != self.le_task_name.text():
            self._task.task_name = self.le_task_name.text()
        if self._task.group_name != self.comb_task_group.currentText():
            self._task.group_name = self.comb_task_group.currentText()
        if self._task.schedule != self.le_task_schedule.text():
            self._task.schedule = self.le_task_schedule.text()
        if self._task.enabled != self.chkb_task_enabled.isChecked():
            self._task.enabled = self.chkb_task_enabled.isChecked()

        # source group
        (server_url, username, password) = self.sw_source.get_server_options()
        if self._task.source_url != server_url:
            self._task.source_url = server_url
        if self._task.source_username != username:
            self._task.source_username = username
        if self._task.source_password != password:
            self._task.source_password = password

        # filter gruop
        if self._task.filter_filename != self.le_filter_filename.text():
            self._task.filter_filename = self.le_filter_filename.text()
        if self._task.filter_valid_time != self.comb_filter_valid_time.currentData():
            self._task.filter_valid_time = self.comb_filter_valid_time.currentData()
        if self._task.subdir_recursion != self.spinBox_subdir_recursion.value():
            self._task.subdir_recursion = self.spinBox_subdir_recursion.value()
        if self._task.middleware != self.comb_middleware.currentData():
            self._task.middleware = self.comb_middleware.currentData()
        if self._task.middleware_arg != self.le_middleware_arg.text():
            self._task.middleware_arg = self.le_middleware_arg.text()
        if self._task.suffix != self.le_suffix.text():
            self._task.suffix = self.le_suffix.text()
        if self._task.processed_reserve_time != int(self.le_processed_reserve.text()):
            self._task.processed_reserve_time = int(self.le_processed_reserve.text())
        if self._task.delete_source != self.chkb_delete_source.isChecked(): 
            self._task.delete_source = self.chkb_delete_source.isChecked()

        # destination group
        (server_url, username, password) = self.sw_dest.get_server_options()
        if self._task.dest_url != server_url:
            self._task.dest_url = server_url
        if self._task.dest_username != username:
            self._task.dest_username = username
        if self._task.dest_password != password:
            self._task.dest_password = password

        return self._task

    def validate_user_input(self) -> str | None:
        """validate user input from dialog.

        Returns:
            str | None: return error message, or None if there is no error.
        """

        self.logger.debug('验证用户输入')

        # 验证 调度时间
        if not croniter.is_valid(self.le_task_schedule.text()):
            self.le_task_schedule.setFocus()
            self.logger.warning('调度时间输入有误: %s', self.le_task_schedule.text())
            return 'Schedule syntax error!'
        self.logger.debug('调度时间验证通过')
        
        # 验证 源服务器地址
        try:
            self.sw_source.get_server_options()
        except Exception as e:
            self.sw_source.le_host.setFocus()
            self.logger.warning('源服务器配置输入有误: %s', str(e))
            return 'Source options error! ' + str(e)
        self.logger.debug('源服务器配置验证通过')
        
        # 验证 文件名正则表达式
        try:
            re.compile(self.le_filter_filename.text())
        except Exception as e:
            self.le_filter_filename.setFocus()
            self.logger.warning('文件名正则表达式有误: %s - %s', self.le_filter_filename.text(), str(e))
            return 'Filter filename regex error! ' + str(e)
        self.logger.debug('文件名正则表达式验证通过')

        # 验证 目标服务器地址
        try:
            self.sw_dest.get_server_options()
        except Exception as e:
            self.sw_dest.le_host.setFocus()
            self.logger.warning('目标服务器配置输入有误: %s', str(e))
            return 'Destination options error! ' + str(e)
        self.logger.debug('目标服务器配置验证通过')

        return None
    
    def accept(self):
        """overwrite QDialog.accept() method. validate user input before accept.
        """
        self.logger.debug('用户点击 accept 按钮，准备对用户输入进行格式验证。')

        msg = self.validate_user_input()
        if msg is None:
            self.logger.debug('格式验证通过')
            super().accept()
        else:
            # QLabel 不支持长字符串的自动 elide 成 'This is long tex...'，要用 QFontMetrics 实现
            self.label_error_msg.setText(QFontMetrics(self.label_error_msg.font()).elidedText(msg, Qt.TextElideMode.ElideRight, 250))
            self.label_error_msg.setToolTip(msg)

    def show_regex_test_dialog(self):
        dialog = DialogRegularExpress(self.le_filter_filename.text())
        dialog.exec()
        pass

def test(arg=None):
    
    from PySide6.QtWidgets import QApplication
    from peewee import SqliteDatabase, fn
    from playhouse.shortcuts import model_to_dict
    
    from transfer_dog.utility.constants import TASK_DB

    logging_format = '%(asctime)s %(levelname)5s %(name)s.%(funcName)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

    Task.bind(SqliteDatabase(str(TASK_DB)))
    app = QApplication(sys.argv)
    dialog = DialogTaskEdit()

    if dialog.exec() == QDialog.DialogCode.Accepted:
        logging.debug("dialog save!")
        task = dialog.retrieve_task()
        logging.debug('task: %s', model_to_dict(task))
    else:
        logging.debug("dialog cancel")

    pass


if __name__ == "__main__":
    test()