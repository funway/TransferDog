#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/08 20:08:18

import logging
from urllib import parse

from PySide6.QtWidgets import QWidget, QLineEdit, QFileDialog
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QIntValidator, QRegularExpressionValidator

from transfer_dog.ui.ui_server_widget import Ui_Form
from transfer_dog.utility.constants import REGEX_IP_ADDRESS


class ServerWidget(QWidget, Ui_Form):

    def __init__(self, server_url, user, password):
        super(ServerWidget, self).__init__()
        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.setupUi(self)

        self.btn_group_protocol.buttonToggled.connect(self.on_protocol_toggled)
        self.chkb_use_keyfile.stateChanged.connect(self.check_keyfile_or_password)
        self.pb_dir.clicked.connect(lambda: self.open_file_dialog_to(self.le_dir))
        self.pb_keyfile.clicked.connect(lambda: self.open_file_dialog_to(self.le_keyfile, is_dir=False))

        # Maybe use host domainname
        # self.le_host.setValidator(QRegularExpressionValidator(REGEX_IP_ADDRESS))
        self.le_port.setValidator(QIntValidator(0, 65535))
        self.le_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.logger.debug('server url: %s', server_url)
        self.update_UI(server_url, user, password)

        pass

    def update_UI(self, server_url, user, password):
        o = parse.urlparse(server_url)
        querys = dict(parse.parse_qsl(o.query))

        # protocol
        if o.scheme == 'local':
            self.rb_local.setChecked(True)
        elif o.scheme == 'ftp' or o.scheme == 'ftps':
            self.rb_ftp.setChecked(True)
            self.chkb_ftps.setChecked(o.scheme == 'ftps')
        elif o.scheme == 'sftp':
            self.rb_sftp.setChecked(True)
        else:
            raise Exception('Unsupported Protocol')
        
        # host, port, user, password
        self.le_host.setText(o.hostname)
        self.le_port.setText(str(o.port) if o.port else None)
        self.le_user.setText(user)
        self.le_password.setText(password)

        # keyfile
        keyfile = querys.get('keyfile', None)
        self.chkb_use_keyfile.setChecked(keyfile is not None)
        self.le_keyfile.setText(keyfile)
        
        # passive mode
        passive = querys.get('passive', 'True')
        self.chkb_passive.setChecked(passive.upper() == 'TRUE')

        # encoding
        encoding = querys.get('encoding', 'UTF8')
        self.comb_encoding.setCurrentText(encoding)

        # directory
        dir = o.path
        self.le_dir.setText(dir)
        
        pass

    def on_protocol_toggled(self, btn, checked):
        """如果按钮组发生 toggle 事件，那么通常会发出两次 toogle 信号，
        先是触发原选中按钮的 unchecked (如果有原选中按钮的话)，然后再触发新选中按钮的 checked。

        Args:
            btn (_type_): 触发信号的按钮
            checked (_type_): 是否选中
        """
        self.logger.debug('btn %s, toggled to %s', btn.objectName(), checked)
        
        if not checked:
            # 如果是按钮被 unchecked
            if btn is self.rb_sftp:
                self.label_password.setEnabled(True)
                self.le_password.setEnabled(True)
            pass
        else:
            # 如果是按钮被 checked
            if btn is self.rb_local:
                self.gp_server.setEnabled(False)
                self.pb_dir.setEnabled(True)
            else:
                self.gp_server.setEnabled(True)
                self.pb_dir.setEnabled(False)
                
                self.label_encoding.setDisabled(btn is self.rb_sftp)
                self.comb_encoding.setDisabled(btn is self.rb_sftp)
                self.comb_encoding.setToolTip('Not supported' if btn is self.rb_sftp else None)

            if btn is self.rb_ftp:
                self.stackedWidget.setCurrentWidget(self.page_ftp)
                self.le_port.setPlaceholderText('21')
            elif btn is self.rb_sftp:
                self.stackedWidget.setCurrentWidget(self.page_sftp)
                self.le_port.setPlaceholderText('22')
                self.check_keyfile_or_password()

        pass

    def check_keyfile_or_password(self):
        """检查 SFTP 使用 password 还是 keyfile 登录

        Args:
            state (_type_): _description_
        """
        self.logger.debug('use_keyfile check state: %s', self.chkb_use_keyfile.checkState())

        use_keyfile = (self.chkb_use_keyfile.checkState() == Qt.CheckState.Checked)
        
        self.le_keyfile.setEnabled(use_keyfile)
        self.pb_keyfile.setEnabled(use_keyfile)
        self.label_password.setDisabled(use_keyfile)
        self.le_password.setDisabled(use_keyfile)
        pass

    def open_file_dialog_to(self, lineEdit: QLineEdit, is_dir: bool = True):
        """为一个文本输入框弹出一个“打开文件对话框”，并将用户选择的路径写入该文本框。

        Args:
            lineEdit (QLineEdit): 目标文本框
            is_dir (bool, optional): 要打开的是目录还是文件. Defaults to True.
        """
        if is_dir:
            path = str(QFileDialog.getExistingDirectory(self, caption='Select Directory'))
        else:
            path = str(QFileDialog.getOpenFileName(self, caption='Select File')[0])
        if path is not None and len(path) != 0:
            lineEdit.setText(path)
        pass

    def get_scheme(self) -> str:
        """返回当前选中的服务器协议

        Returns:
            str: local/ftp/ftps/sftp
        """
        scheme = self.btn_group_protocol.checkedButton().text().lower()
        
        if self.btn_group_protocol.checkedButton() is self.rb_ftp:
            if self.chkb_ftps.isChecked():
                scheme = 'ftps'
            else:
                scheme = 'ftp'

        self.logger.debug('scheme: (%s)', scheme)
        return scheme
    
    def get_netloc(self):
        netloc = self.le_host.text() 
        netloc += '' if self.le_port.text() == '' else ':%s'%self.le_port.text()
        
        if self.rb_local.isChecked():
            # netloc = ''
            netloc = '127.0.0.1'

        self.logger.debug('netloc: (%s)', netloc)
        return netloc
    
    def get_query(self):
        query = ''

        if self.rb_ftp.isChecked():
            query = 'encoding=%s&passive=%s' % (self.comb_encoding.currentText(), 
                                                 self.chkb_passive.isChecked())
        if self.rb_sftp.isChecked():
            # query = 'encoding=%s' % self.comb_encoding.currentText()
            # TODO SFTP library prarmiko do not support other encoding now. (´･_･`)
            query = 'encoding=UTF8'
            if self.chkb_use_keyfile.isChecked():
                query += '&keyfile=' + self.le_keyfile.text()
        
        self.logger.debug('query: (%s)', query)
        return query

    def validate_user_input(self, throw_error = False) -> str | None:
        """验证用户输入.

        Args:
            throw_error (bool, optional): 是否抛出异常. Defaults to False.

        Raises:
            e: _description_

        Returns:
            str | None: return error message, or None if there is no error.
        """
        self.logger.debug('验证用户输入')

        # 验证 源服务器地址
        try:
            o = parse.ParseResult(
                    scheme = self.get_scheme(),
                    netloc = self.get_netloc(),
                    path = self.le_dir.text(),
                    params = '',
                    query = self.get_query(),
                    fragment = ''
                )
            o.port  # urlparse 执行时不会对 port 错误抛出异常，只有在调用 port 的时候才会。
        except Exception as e:
            if throw_error:
                raise e
            else:
                self.le_host.setFocus()
                self.logger.warning('server options parse error: %s', str(e))
                return 'Server options error! ' + str(e)
        pass
    
    def get_server_options(self) -> tuple:
        """获取服务器信息 (server_url, username, password)

        Raises:
            e: 解析用户输入时可能抛出异常

        Returns:
            tuple: 返回三元组 (server_url, username, password)
        """
        try:
            o = parse.ParseResult(
                    scheme = self.get_scheme(),
                    netloc = self.get_netloc(),
                    path = self.le_dir.text(),
                    params = '',
                    query = self.get_query(),
                    fragment = ''
                )
            o.port  # urlparse 执行时不会对 port 错误抛出异常，只有在调用 port 的时候才会。
        except Exception as e:
            self.logger.exception('获取服务器信息时发生异常')
            raise e
        else:
            server_url = parse.urlunparse(o)
            username = None if self.rb_local.isChecked() else self.le_user.text()
            password = None if self.rb_local.isChecked() else self.le_password.text()
            return (server_url, username, password)

    def test(self):
        print(self.get_server_options())
        pass
