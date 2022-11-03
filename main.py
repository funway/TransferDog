#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/11/03 20:23:34

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for MainWindow."""
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setupUi(self)
        pass
    

def main(arg=None):
    
    # 生成QApplication主程序
    app = QApplication(sys.argv)
    
    # 生成并显示主窗口
    main_window = MainWindow()
    main_window.show()

    # 进入主程序循环直到退出
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()