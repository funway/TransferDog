#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 22:11:21

import sys, logging
from PyQt6.QtWidgets import QApplication, QDialog
from ui.ui_task_edit_dialog import Ui_Dialog


class TaskEditDialog(QDialog, Ui_Dialog):
    """docstring for TaskEditDialog."""
    def __init__(self):
        super(TaskEditDialog, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance' % self.__class__.__name__)

        # 装载 UI
        self.setupUi(self)

        # 绑定 信号-槽
        self.rbSourceFtp.toggled.connect(lambda: self.stSource.setCurrentIndex(0))
        self.rbSourceLocal.toggled.connect(lambda: self.stSource.setCurrentIndex(1))
        self.rbDestFtp.toggled.connect(lambda: self.stDestination.setCurrentIndex(0))
        self.rbDestLocal.toggled.connect(lambda: self.stDestination.setCurrentIndex(1))
        pass


def main(arg=None):
    """ test qdialog """

    app = QApplication(sys.argv)
    dialog = TaskEditDialog()

    if dialog.exec() == QDialog.DialogCode.Accepted:
        print("dialog save!")
        print("task name: %s" % dialog.lineEditTaskName.text())
    else:
        print("dialog cancel")

    pass

if __name__ == "__main__":
    main()