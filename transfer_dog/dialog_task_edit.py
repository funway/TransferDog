#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/01/11 19:56:02

import logging
from PyQt6.QtWidgets import QDialog
from ui.ui_dialog_task_edit import Ui_Dialog


class DialogTaskEdit(QDialog, Ui_Dialog):
    """docstring for DialogTaskEdit."""
    def __init__(self):
        super(DialogTaskEdit, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance' % self.__class__.__name__)

        # 装载 UI
        self.setupUi(self)

        # 绑定 信号-槽
        # self.rbSourceFtp.toggled.connect(lambda: self.stSource.setCurrentIndex(0))
        # self.rbSourceLocal.toggled.connect(lambda: self.stSource.setCurrentIndex(1))
        # self.rbDestFtp.toggled.connect(lambda: self.stDestination.setCurrentIndex(0))
        # self.rbDestLocal.toggled.connect(lambda: self.stDestination.setCurrentIndex(1))

        pass

    