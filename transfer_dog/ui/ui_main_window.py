# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLineEdit,
    QMainWindow, QSizePolicy, QStatusBar, QTableView,
    QToolBar, QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"")
        self.actionNewTask = QAction(MainWindow)
        self.actionNewTask.setObjectName(u"actionNewTask")
        icon = QIcon()
        icon.addFile(u"/transfer_dog/resource/img/file-add-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNewTask.setIcon(icon)
        self.actionEditTask = QAction(MainWindow)
        self.actionEditTask.setObjectName(u"actionEditTask")
        icon1 = QIcon()
        icon1.addFile(u"transfer_dog/resource/img/file-edit-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionEditTask.setIcon(icon1)
        self.actionTest = QAction(MainWindow)
        self.actionTest.setObjectName(u"actionTest")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.lineEdit)

        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout.addWidget(self.treeView)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")

        self.horizontalLayout.addWidget(self.tableView)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.toolBar.addAction(self.actionNewTask)
        self.toolBar.addAction(self.actionEditTask)
        self.toolBar.addAction(self.actionTest)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNewTask.setText(QCoreApplication.translate("MainWindow", u"NewTask", None))
#if QT_CONFIG(tooltip)
        self.actionNewTask.setToolTip(QCoreApplication.translate("MainWindow", u"Add new transfer task", None))
#endif // QT_CONFIG(tooltip)
        self.actionEditTask.setText(QCoreApplication.translate("MainWindow", u"EditTask", None))
#if QT_CONFIG(tooltip)
        self.actionEditTask.setToolTip(QCoreApplication.translate("MainWindow", u"Edit a task's property", None))
#endif // QT_CONFIG(tooltip)
        self.actionTest.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Task", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

