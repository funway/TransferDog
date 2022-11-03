#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 22:11:21

import sys
from PyQt6.QtWidgets import QApplication, QDialog
from ui.ui_task_edit_dialog import Ui_Dialog


class TaskEditDialog(QDialog, Ui_Dialog):
    """docstring for TaskEditDialog."""
    def __init__(self):
        super(TaskEditDialog, self).__init__()
        self.setupUi(self)
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