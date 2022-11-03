#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from ui.ui_main_window import Ui_MainWindow
from task_edit_dialog import TaskEditDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setupUi(self)
        
        # 绑定信号-槽
        self.actionNewTask.triggered.connect(self.slot_show_edit_task_dialog)

        pass

    def slot_show_edit_task_dialog(self):
        
        dialog = TaskEditDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            print("dialog save!")
            print("task name: %s" % dialog.lineEditTaskName.text())
        else:
            print("dialog cancel")

        pass
    

def main(arg=None):
    
    # 生成QApplication主程序
    app = QApplication(sys.argv)
    
    # 生成并显示主窗口
    main_window = MainWindow()

    # 加载 stylesheet
    with open(os.path.dirname(__file__) + '/ui/resources/stylesheets/default.qss', 'r') as qss_file:
        qss = qss_file.read()
        app.setStyleSheet(qss)

    main_window.show()

    # 进入主程序循环直到退出
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()