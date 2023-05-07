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
from urllib import parse

from croniter import croniter
from peewee import fn
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QDialog, QFileDialog, QLineEdit

from transfer_dog.ui.ui_dialog_task_edit import Ui_Dialog
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

        # 绑定 信号-槽
        self.buttonGroup_src_protocol.buttonToggled.connect(self.on_src_protocol_toggled)
        self.buttonGroup_dest_protocol.buttonToggled.connect(self.on_dest_protocol_toggled)
        self.pushButton_src_browse.clicked.connect(lambda: self.open_file_dialog_to(self.lineEdit_src_dir))
        self.pushButton_dest_browse.clicked.connect(lambda: self.open_file_dialog_to(self.lineEdit_dest_dir))

        # 根据 _task 更新 UI
        self.update_UI()
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

    def update_UI(self):
        """Update dialog UI according to the self._task. Do some UI updating that cannot be done in setupUI().
        """        
        task = self._task

        #   初始化任务分组下拉框
        groups = [row['group_name'] for row in Task.select( fn.Distinct(Task.group_name) ).dicts()]
        groups.sort()
        self.comboBox_task_group.addItems(groups)

        # update general group
        self.lineEdit_task_name.setText(task.task_name)
        self.comboBox_task_group.setCurrentText(task.group_name)
        self.lineEdit_task_schedule.setText(task.schedule)
        self.checkBox_task_enabled.setChecked(task.enabled)

        # update source group
        o = parse.urlparse(task.source_url)
        if o.scheme == 'local':
            self.radioButton_src_local.setChecked(True)
        elif o.scheme == 'ftp':
            self.radioButton_src_ftp.setChecked(True)
        elif o.scheme == 'sftp':
            self.radioButton_src_sftp.setChecked(True)
        self.lineEdit_src_server_netloc.setText(o.netloc)
        querys = dict(parse.parse_qsl(o.query))
        self.comboBox_src_server_encoding.setCurrentText(querys.get('encoding', 'UTF8'))
        self.checkBox_src_server_passive.setChecked(querys.get('passive', 'False').upper() == 'TRUE')
        self.lineEdit_src_dir.setText(o.path)

        # update filter group
        #   文件名过滤
        self.lineEdit_filter_filename.setText(task.filter_filename)
        #   子目录递归
        self.spinBox_subdir_recursion.setValue(task.subdir_recursion)
        #   删除源文件
        self.checkBox_delete_source.setChecked(task.delete_source)
        #   有效时间过滤
        for key, text in task_valid_time_options.items():
            self.comboBox_filter_valid_time.addItem(text, key)
        try:
            self.comboBox_filter_valid_time.setCurrentText(task_valid_time_options[self._task.filter_valid_time])
        except Exception as e:
            logging.exception('task.filter_valid_time 异常！无法找到对应的选项')
            self.comboBox_filter_valid_time.setCurrentIndex(0)
        #   中间件
        self.comboBox_middleware.addItem('None', None)
        middlewares = [fname.name for fname in MIDDLEWARE_PATH.glob('*.py')]
        middlewares.sort()
        for mw in middlewares:
            self.comboBox_middleware.addItem(mw, mw)
        self.comboBox_middleware.setCurrentIndex(self.comboBox_middleware.findText('None' if task.middleware is None else task.middleware))
        self.lineEdit_middleware_arg.setText(task.middleware_arg)

        # update destination group
        o = parse.urlparse(task.dest_url)
        if o.scheme == 'local':
            # 由 radioButton.setChecked 触发 buttonGroup.buttonToggled 信号
            self.radioButton_dest_local.setChecked(True)
        elif o.scheme == 'ftp':
            self.radioButton_dest_ftp.setChecked(True)
        elif o.scheme == 'sftp':
            self.radioButton_dest_sftp.setChecked(True)
        self.lineEdit_dest_server_netloc.setText(o.netloc)
        querys = dict(parse.parse_qsl(o.query))
        self.comboBox_dest_server_encoding.setCurrentText(querys.get('encoding', 'UTF8'))
        self.checkBox_dest_server_passive.setChecked( querys.get('passive', 'False').upper() == 'TRUE' )
        self.lineEdit_dest_dir.setText(o.path)

        pass

    def on_src_protocol_toggled(self, btn, checked):
        """Signal/Slot 槽函数，根据用户选择的服务器协议类型，自动 enable/disable 部分用户设置。
        注意，当用户切换选中的 QRadioButton 时, QButtonGroup::buttonToggled 会触发两次。
        一次代表 A toggled to False, 一次代表 B toggled to True. 

        Args:
            btn (_type_): 代表用户点击的 QRadioButton 按钮
            checked (bool): 该按钮是被 Checked 还是 Unchecked
        """
        self.logger.debug('btn %s, toggled to %s', btn.objectName(), checked)

        if not checked:
            # Toggled to False 的不处理
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

    def on_dest_protocol_toggled(self, btn, checked):
        self.logger.debug('btn %s, toggled to %s', btn.objectName(), checked)
        
        if not checked:
            # Toggled to False 的不处理
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
    
    def retrieve_task(self) -> Task:
        """从对话框实例中获取 Task 实例。

        Returns:
            Task: 返回 self._task。在返回之前，需要先从对话框面板获取更新数据。
        """

        # general group
        if self._task.task_name != self.lineEdit_task_name.text():
            self._task.task_name = self.lineEdit_task_name.text()
        if self._task.group_name != self.comboBox_task_group.currentText():
            self._task.group_name = self.comboBox_task_group.currentText()
        if self._task.schedule != self.lineEdit_task_schedule.text():
            self._task.schedule = self.lineEdit_task_schedule.text()
        if self._task.enabled != self.checkBox_task_enabled.isChecked():
            self._task.enabled = self.checkBox_task_enabled.isChecked()

        # source group
        source_url = parse.urlunparse(parse.ParseResult(
            scheme = self.buttonGroup_src_protocol.checkedButton().text().lower(),
            netloc = self.lineEdit_src_server_netloc.text(),
            path = self.lineEdit_src_dir.text(),
            params = '',
            query = parse.urlencode({ 'encoding': self.comboBox_src_server_encoding.currentText(),
                                      'passive': self.checkBox_src_server_passive.isChecked() }),
            fragment = ''
        ))
        if self._task.source_url != source_url:
            self._task.source_url = source_url
        self.logger.debug('Get source url: %s', source_url)

        # filter gruop
        if self._task.filter_filename != self.lineEdit_filter_filename.text():
            self._task.filter_filename = self.lineEdit_filter_filename.text()
        if self._task.filter_valid_time != self.comboBox_filter_valid_time.currentData():
            self._task.filter_valid_time = self.comboBox_filter_valid_time.currentData()
        if self._task.subdir_recursion != self.spinBox_subdir_recursion.value():
            self._task.subdir_recursion = self.spinBox_subdir_recursion.value()
        if self._task.delete_source != self.checkBox_delete_source.isChecked(): 
            self._task.delete_source = self.checkBox_delete_source.isChecked()
        if self._task.middleware != self.comboBox_middleware.currentData():
            self._task.middleware = self.comboBox_middleware.currentData()
        if self._task.middleware_arg != self.lineEdit_middleware_arg.text():
            self._task.middleware_arg = self.lineEdit_middleware_arg.text()

        # destination group
        dest_url = parse.urlunparse(parse.ParseResult(
            scheme = self.buttonGroup_dest_protocol.checkedButton().text().lower(),
            netloc = self.lineEdit_dest_server_netloc.text(),
            path = self.lineEdit_dest_dir.text(),
            params = '',
            query = parse.urlencode({ 'encoding': self.comboBox_dest_server_encoding.currentText(),
                                      'passive': self.checkBox_dest_server_passive.isChecked() }),
            fragment = ''
        ))
        if self._task.dest_url != dest_url:
            self._task.dest_url = dest_url
        self.logger.debug('Get dest url: %s', dest_url)

        return self._task

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
            o = parse.ParseResult(
                    scheme = self.buttonGroup_src_protocol.checkedButton().text().lower(),
                    netloc = self.lineEdit_src_server_netloc.text(),
                    path = self.lineEdit_src_dir.text(),
                    params = '',
                    query = parse.urlencode({ 'encoding': self.comboBox_src_server_encoding.currentText(),
                                            'passive': self.checkBox_src_server_passive.isChecked() }),
                    fragment = ''
                )
            o.port # urlparse 执行时不会对 port 错误抛出异常，只有在调用 port 的时候才会。
        except Exception as e:
            self.lineEdit_src_server_netloc.setFocus()
            self.logger.warning('源服务器地址输入有误: %s - %s', self.lineEdit_src_server_netloc.text(), str(e))
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
            o = parse.ParseResult(
                    scheme = self.buttonGroup_dest_protocol.checkedButton().text().lower(),
                    netloc = self.lineEdit_dest_server_netloc.text(),
                    path = self.lineEdit_dest_dir.text(),
                    params = '',
                    query = parse.urlencode({ 'encoding': self.comboBox_dest_server_encoding.currentText(),
                                            'passive': self.checkBox_dest_server_passive.isChecked() }),
                    fragment = ''
                )
            o.port # urlparse 执行时不会对 port 错误抛出异常，只有在调用 port 的时候才会。
        except Exception as e:
            self.lineEdit_dest_server_netloc.setFocus()
            self.logger.warning('目标服务器地址输入有误: %s - %s', self.lineEdit_dest_server_netloc.text(), str(e))
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
    
    from PySide6.QtWidgets import QApplication
    from peewee import SqliteDatabase, fn
    from playhouse.shortcuts import model_to_dict
    
    from transfer_dog.utility.constants import TASK_DB

    logging_format = '%(asctime)s %(levelname)5s %(name)s.%(funcName)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

    Task.bind(SqliteDatabase(str(TASK_DB)))
    app = QApplication(sys.argv)
    dialog = DialogTaskEdit()

    groups = [row['group_name'] for row in Task.select( fn.Distinct(Task.group_name) ).dicts()]
    logging.info(groups)

    from transfer_dog.utility.constants import PROJECT_PATH
    for f in (PROJECT_PATH / 'plugin/middleware').glob('*.py'):
        logging.info(f.name)


    if dialog.exec() == QDialog.DialogCode.Accepted:
        logging.debug("dialog save!")
        task = dialog.retrieve_task()
        logging.debug('task: %s', model_to_dict(task))
    else:
        logging.debug("dialog cancel")

    pass


if __name__ == "__main__":
    test()