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
        icon.addFile(u"../transfer_dog/resource/img/file-add-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNewTask.setIcon(icon)
        self.actionEditTask = QAction(MainWindow)
        self.actionEditTask.setObjectName(u"actionEditTask")
        icon1 = QIcon()
        icon1.addFile(u"../transfer_dog/resource/img/file-edit-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionEditTask.setIcon(icon1)
        self.actionTest = QAction(MainWindow)
        self.actionTest.setObjectName(u"actionTest")
        icon2 = QIcon()
        icon2.addFile(u"../transfer_dog/resource/img/question-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionTest.setIcon(icon2)
        self.actionDeleteTask = QAction(MainWindow)
        self.actionDeleteTask.setObjectName(u"actionDeleteTask")
        icon3 = QIcon()
        icon3.addFile(u"../transfer_dog/resource/img/file-reduce-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDeleteTask.setIcon(icon3)
        self.actionOpenSource = QAction(MainWindow)
        self.actionOpenSource.setObjectName(u"actionOpenSource")
        icon4 = QIcon()
        icon4.addFile(u"../transfer_dog/resource/img/folder-download-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpenSource.setIcon(icon4)
        self.actionOpenDest = QAction(MainWindow)
        self.actionOpenDest.setObjectName(u"actionOpenDest")
        icon5 = QIcon()
        icon5.addFile(u"../transfer_dog/resource/img/folder-upload-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpenDest.setIcon(icon5)
        self.actionCopyTask = QAction(MainWindow)
        self.actionCopyTask.setObjectName(u"actionCopyTask")
        icon6 = QIcon()
        icon6.addFile(u"../transfer_dog/resource/img/file-copy-2-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionCopyTask.setIcon(icon6)
        self.actionStopTask = QAction(MainWindow)
        self.actionStopTask.setObjectName(u"actionStopTask")
        icon7 = QIcon()
        icon7.addFile(u"../transfer_dog/resource/img/stop-circle-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStopTask.setIcon(icon7)
        self.actionStartTask = QAction(MainWindow)
        self.actionStartTask.setObjectName(u"actionStartTask")
        icon8 = QIcon()
        icon8.addFile(u"../transfer_dog/resource/img/play-circle-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStartTask.setIcon(icon8)
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
        self.toolBar.addAction(self.actionCopyTask)
        self.toolBar.addAction(self.actionDeleteTask)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStartTask)
        self.toolBar.addAction(self.actionStopTask)
        self.toolBar.addAction(self.actionOpenSource)
        self.toolBar.addAction(self.actionOpenDest)
        self.toolBar.addSeparator()
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
        self.actionDeleteTask.setText(QCoreApplication.translate("MainWindow", u"DeleteTask", None))
#if QT_CONFIG(tooltip)
        self.actionDeleteTask.setToolTip(QCoreApplication.translate("MainWindow", u"Delete selected task", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpenSource.setText(QCoreApplication.translate("MainWindow", u"OpenSource", None))
#if QT_CONFIG(tooltip)
        self.actionOpenSource.setToolTip(QCoreApplication.translate("MainWindow", u"Open source path", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpenDest.setText(QCoreApplication.translate("MainWindow", u"OpenDest", None))
#if QT_CONFIG(tooltip)
        self.actionOpenDest.setToolTip(QCoreApplication.translate("MainWindow", u"Open destination path", None))
#endif // QT_CONFIG(tooltip)
        self.actionCopyTask.setText(QCoreApplication.translate("MainWindow", u"CopyTask", None))
        self.actionStopTask.setText(QCoreApplication.translate("MainWindow", u"StopTask", None))
        self.actionStartTask.setText(QCoreApplication.translate("MainWindow", u"StartTask", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Task", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

