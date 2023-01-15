#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/01/11 19:56:02

import logging
from urllib.parse import urlparse
from datetime import datetime

import croniter
from PyQt6.QtWidgets import QDialog, QFileDialog

from models.task import Task
from ui.ui_dialog_task_edit import Ui_Dialog


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
        self.logger.debug('Init a %s instance' % self.__class__.__name__)

        # 定义成员变量
        if task is None:
            self.__task = Task()
            self.logger.debug('新建任务. [%s]', self.__task.uuid)
        else:
            self.__task = task
            self.logger.debug('修改任务. [%s]', self.__task.uuid)

        # 装载 UI
        self.setupUi(self)
        self.update_UI()

        # 绑定 信号-槽
        self.buttonGroup_src_protocol.buttonToggled.connect(self.update_groupBox_src_server)
        self.buttonGroup_dest_protocol.buttonToggled.connect(self.update_groupBox_dest_server)
        self.pushButton_src_dir.clicked.connect(lambda: self.open_file_dialog_to(self.lineEdit_src_dir))
        self.pushButton_dest_dir.clicked.connect(lambda: self.open_file_dialog_to(self.lineEdit_dest_dir))

        pass

    def open_file_dialog_to(self, lineEdit):
        path = str(QFileDialog.getExistingDirectory(self, caption='Select Directory'))
        if path is not None and len(path) != 0:
            lineEdit.setText(path)
        pass

    def retrieve_task(self) -> Task:
        """从对话框实例中获取 Task 实例。

        Returns:
            Task: 返回 self.__task。在返回之前，需要先从对话框面板获取更新数据。
        """
        self.__task.task_name = self.lineEdit_task_name.text()
        self.__task.group_name = self.comboBox_task_group.currentText()
        self.__task.schedule = self.lineEdit_task_schedule.text()
        self.__task.enabled = self.checkBox_task_enabled.isChecked()

        self.__task.filter_valid_time = self.comboBox_filter_valid_time.currentData()

        return self.__task

    def update_UI(self):
        """update dialog UI according to the self.__task.
        """
        
        # 执行 setupUI() 无法完成的其他初始化设置
        #   初始化任务分组下拉框
        self.comboBox_task_group.addItem('Default')
        #   初始化有效时间下拉框
        for key, text in task_valid_time_options.items():
            self.comboBox_filter_valid_time.addItem(text, key)

        task = self.__task
        self.lineEdit_task_name.setText(task.task_name)
        self.comboBox_task_group.setCurrentText(task.group_name)
        self.lineEdit_task_schedule.setText(task.schedule)
        self.checkBox_task_enabled.setChecked(task.enabled)

        o = urlparse(task.source_server)
        if o.scheme == 'local':
            self.radioButton_src_local.setChecked(True)
        elif o.scheme == 'ftp':
            self.radioButton_src_ftp.setChecked(True)
        elif o.scheme == 'sftp':
            self.radioButton_src_sftp.setChecked(True)
        self.lineEdit_src_server_address.setText(o.netloc)
        self.comboBox_src_server_encoding.setCurrentText(task.source_encoding)
        self.checkBox_src_server_passive.setChecked(task.source_passive_mode)
        self.lineEdit_src_dir.setText(task.source_path)

        self.lineEdit_filter_filename.setText(task.filter_filename)
        self.checkBox_scan_subdir.setChecked(task.scan_subdir)
        self.checkBox_delete_source.setChecked(task.delete_source)
        try:
            self.comboBox_filter_valid_time.setCurrentText(task_valid_time_options[self.__task.filter_valid_time])
        except Exception as e:
            logging.exception('task.filter_valid_time 异常！无法找到对应的选项')
            self.comboBox_filter_valid_time.setCurrentIndex(0)

        o = urlparse(task.dest_server)
        if o.scheme == 'local':
            self.radioButton_src_local.setChecked(True)
        elif o.scheme == 'ftp':
            self.radioButton_src_ftp.setChecked(True)
        elif o.scheme == 'sftp':
            self.radioButton_src_sftp.setChecked(True)
        self.lineEdit_dest_server_address.setText(o.netloc)
        self.comboBox_dest_server_encoding.setCurrentText(task.dest_encoding)
        self.checkBox_dest_server_passive.setChecked(task.dest_passive_mode)
        self.lineEdit_dest_dir.setText(task.dest_path)

        pass

    def update_groupBox_src_server(self, btn, checked):
        self.logger.debug('btn %s, toggled to %s', btn.objectName(), checked)

        if not checked:
            return
        elif btn is self.radioButton_src_local:
            self.logger.debug('radioButton_src_local checked!')
            self.groupBox_src_server.setEnabled(False)
        else:
            self.logger.debug('radioButton_src_ftp/sftp checked!')
            self.groupBox_src_server.setEnabled(True)
        pass

    def update_groupBox_dest_server(self, btn, checked):
        self.logger.debug('btn %s, toggled to %s', btn.objectName(), checked)
        
        if not checked:
            return
        elif btn is self.radioButton_dest_local:
            self.logger.debug('radioButton_dest_local checked!')
            self.groupBox_dest_server.setEnabled(False)
        else:
            self.logger.debug('radioButton_dest_ftp/sftp checked!')
            self.groupBox_dest_server.setEnabled(True)

        pass

    def validate_user_input(self):
        
        if not croniter.is_valid(self.lineEdit_task_schedule.text()):
            return 'schedule syntax error!'

        pass
    
    def accept(self):
        """overwrite QDialog.accept() method. validate user input before accept.
        """
        self.logger.debug('用户点击 accept 按钮，准备对用户输入进行格式验证。')

        super().accept()


def test(arg=None):

    import sys
    
    from PyQt6.QtWidgets import QApplication

    logging_format = '%(asctime)s %(levelname)5s %(name)s.%(funcName)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

    app = QApplication(sys.argv)
    dialog = DialogTaskEdit()

    if dialog.exec() == QDialog.DialogCode.Accepted:
        logging.debug("dialog save!")
    else:
        logging.debug("dialog cancel")

    pass


if __name__ == "__main__":
    test()