#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/01/11 19:56:02

import logging, re
from urllib.parse import urlparse

from croniter import croniter
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QDialog, QFileDialog, QButtonGroup, QLineEdit

from model.task import Task
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
            self.logger.debug('新建任务. [%s] %s', self.__task.uuid, self.__task)
        else:
            self.__task = task
            self.logger.debug('修改任务. [%s]', self.__task.uuid)

        # 装载 UI
        self.setupUi(self)
        self.update_UI()

        # 绑定 信号-槽
        self.buttonGroup_src_protocol.buttonToggled.connect(self.update_groupBox_src_server)
        self.buttonGroup_dest_protocol.buttonToggled.connect(self.update_groupBox_dest_server)
        self.pushButton_src_browse.clicked.connect(lambda: self.open_file_dialog_to(self.lineEdit_src_dir))
        self.pushButton_dest_browse.clicked.connect(lambda: self.open_file_dialog_to(self.lineEdit_dest_dir))

        pass

    def open_file_dialog_to(self, lineEdit: QLineEdit):
        """为一个文本输入框弹出一个“打开文件对话框”，并将用户选择的路径写入该文本框。

        Args:
            lineEdit (QLineEdit): 目标文本框
        """
        path = str(QFileDialog.getExistingDirectory(self, caption='Select Directory'))
        if path is not None and len(path) != 0:
            lineEdit.setText(path)
        pass

    def retrieve_task(self) -> Task:
        """从对话框实例中获取 Task 实例。

        Returns:
            Task: 返回 self.__task。在返回之前，需要先从对话框面板获取更新数据。
        """

        # general group
        self.__task.task_name = self.lineEdit_task_name.text()
        self.__task.group_name = self.comboBox_task_group.currentText()
        self.__task.schedule = self.lineEdit_task_schedule.text()
        self.__task.enabled = self.checkBox_task_enabled.isChecked()

        # source group
        self.__task.source_server = self.get_server_url(self.buttonGroup_src_protocol, self.lineEdit_src_server_address)
        self.__task.source_encoding = self.comboBox_src_server_encoding.currentText()
        self.__task.source_passive_mode = self.checkBox_src_server_passive.isChecked()
        self.__task.source_path = self.lineEdit_src_dir.text()


        # filter gruop
        self.__task.filter_filename = self.lineEdit_filter_filename.text()
        self.__task.filter_valid_time = self.comboBox_filter_valid_time.currentData()
        self.__task.scan_subdir = self.checkBox_scan_subdir.isChecked()
        self.__task.delete_source = self.checkBox_delete_source.isChecked()

        # destination group
        self.__task.dest_server = self.get_server_url(self.buttonGroup_dest_protocol, self.lineEdit_dest_server_address)
        self.__task.dest_encoding = self.comboBox_dest_server_encoding.currentText()
        self.__task.dest_passive_mode = self.checkBox_dest_server_passive.isChecked()
        self.__task.dest_path = self.lineEdit_dest_dir.text()

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

        # update general group
        self.lineEdit_task_name.setText(task.task_name)
        self.comboBox_task_group.setCurrentText(task.group_name)
        self.lineEdit_task_schedule.setText(task.schedule)
        self.checkBox_task_enabled.setChecked(task.enabled)

        # update source group
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

        # update filter group
        self.lineEdit_filter_filename.setText(task.filter_filename)
        self.checkBox_scan_subdir.setChecked(task.scan_subdir)
        self.checkBox_delete_source.setChecked(task.delete_source)
        try:
            self.comboBox_filter_valid_time.setCurrentText(task_valid_time_options[self.__task.filter_valid_time])
        except Exception as e:
            logging.exception('task.filter_valid_time 异常！无法找到对应的选项')
            self.comboBox_filter_valid_time.setCurrentIndex(0)

        # update destination group
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
        """Signal/Slot 槽函数，根据用户选择的服务器协议类型，自动 enable/disable 部分用户设置。

        Args:
            btn (_type_): 代表用户点击的 QRadioButton 按钮
            checked (_type_): 该按钮是被 Checked 还是 Unchecked
        """
        # self.logger.debug('btn %s, toggled to %s', btn.objectName(), checked)

        if not checked:
            return
        elif btn is self.radioButton_src_local:
            self.logger.debug('radioButton_src_local checked!')
            self.groupBox_src_server.setEnabled(False)
            self.pushButton_src_browse.setEnabled(True)
        else:
            self.logger.debug('radioButton_src_ftp/sftp checked!')
            self.groupBox_src_server.setEnabled(True)
            self.pushButton_src_browse.setEnabled(False)
        pass

    def update_groupBox_dest_server(self, btn, checked):
        # self.logger.debug('btn %s, toggled to %s', btn.objectName(), checked)
        
        if not checked:
            return
        elif btn is self.radioButton_dest_local:
            self.logger.debug('radioButton_dest_local checked!')
            self.groupBox_dest_server.setEnabled(False)
            self.pushButton_dest_browse.setEnabled(True)
        else:
            self.logger.debug('radioButton_dest_ftp/sftp checked!')
            self.groupBox_dest_server.setEnabled(True)
            self.pushButton_dest_browse.setEnabled(False)

        pass
    
    def get_server_url(self, btng:QButtonGroup, le:QLineEdit) -> str:
        """从 服务器协议选择按钮 与 服务器地址文本框 中获取服务器 URL 地址。

        Args:
            btng (QButtonGroup): 选择协议的 QRadioButton group
            le (QLineEdit): 地址输入框

        Returns:
            str: 以 protocol://address 的格式返回 URL 字符串。
        """
        protocol = btng.checkedButton().text().lower()
        return protocol + '://' + le.text()

    def validate_user_input(self) -> str | None:
        """validate user input from dialog.

        Returns:
            str | None: return error message, or None if there is no error.
        """

        self.logger.debug('验证用户输入')

        # 验证 调度时间
        if not croniter.is_valid(self.lineEdit_task_schedule.text()):
            self.lineEdit_task_schedule.setFocus()
            self.logger.warning('调度时间输入有误: %s', self.lineEdit_task_schedule.text())
            return 'Schedule syntax error!'
        self.logger.debug('调度时间验证通过')
        
        # 验证 源服务器地址
        try:
            o = urlparse(self.get_server_url(self.buttonGroup_src_protocol, self.lineEdit_src_server_address))
            if o.scheme != 'local':
                assert o.hostname is not None, 'Host is None.'
            o.port # urlparse 执行时不会对 port 错误抛出异常，只有在调用 port 的时候才会。
        except Exception as e:
            self.lineEdit_src_server_address.setFocus()
            self.logger.warning('源服务器地址输入有误: %s - %s', self.lineEdit_src_server_address.text(), str(e))
            return 'Source address error! ' + str(e)
        self.logger.debug('源服务器地址验证通过')
        
        # 验证 文件名正则表达式
        try:
            re.compile(self.lineEdit_filter_filename.text())
        except Exception as e:
            self.lineEdit_filter_filename.setFocus()
            self.logger.warning('文件名正则表达式有误: %s - %s', self.lineEdit_filter_filename.text(), str(e))
            return 'Filter filename regex error! ' + str(e)
        self.logger.debug('文件名正则表达式验证通过')

        # 验证 目标服务器地址
        try:
            o = urlparse(self.get_server_url(self.buttonGroup_dest_protocol, self.lineEdit_dest_server_address))
            if o.scheme != 'local':
                assert o.hostname is not None, 'Host is None.'
            o.port # urlparse 执行时不会对 port 错误抛出异常，只有在调用 port 的时候才会。
        except Exception as e:
            self.lineEdit_dest_server_address.setFocus()
            self.logger.warning('目标服务器地址输入有误: %s - %s', self.lineEdit_dest_server_address.text(), str(e))
            return 'Destination address error! ' + str(e)
        self.logger.debug('目标服务器地址验证通过')

        return None
    
    def accept(self):
        """overwrite QDialog.accept() method. validate user input before accept.
        """
        self.logger.debug('用户点击 accept 按钮，准备对用户输入进行格式验证。')

        msg = self.validate_user_input()
        if msg is None:
            super().accept()
        else:
            # QLabel 不支持长字符串的自动 elide 成 'This is long tex...'，要用 QFontMetrics 实现
            self.label_error_msg.setText(QFontMetrics(self.label_error_msg.font()).elidedText(msg, Qt.TextElideMode.ElideRight, 250))
            self.label_error_msg.setToolTip(msg)

def test(arg=None):

    import sys
    
    from PySide6.QtWidgets import QApplication
    from playhouse.shortcuts import model_to_dict

    logging_format = '%(asctime)s %(levelname)5s %(name)s.%(funcName)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

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