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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLineEdit, QMainWindow, QSizePolicy,
    QSplitter, QStatusBar, QTableWidget, QTableWidgetItem,
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
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName(u"actionHelp")
        icon2 = QIcon()
        icon2.addFile(u"../transfer_dog/resource/img/question-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionHelp.setIcon(icon2)
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
        self.actionOpenLogFile = QAction(MainWindow)
        self.actionOpenLogFile.setObjectName(u"actionOpenLogFile")
        icon9 = QIcon()
        icon9.addFile(u"../transfer_dog/resource/img/bug-2-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpenLogFile.setIcon(icon9)
        self.actionOpenProcessedDB = QAction(MainWindow)
        self.actionOpenProcessedDB.setObjectName(u"actionOpenProcessedDB")
        icon10 = QIcon()
        icon10.addFile(u"../transfer_dog/resource/img/git-repository-commits-line.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpenProcessedDB.setIcon(icon10)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.lineEdit)

        self.treeView = QTreeView(self.layoutWidget)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout.addWidget(self.treeView)

        self.splitter.addWidget(self.layoutWidget)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tb_processed = QTableWidget(self.frame)
        self.tb_processed.setObjectName(u"tb_processed")
        self.tb_processed.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_2.addWidget(self.tb_processed)

        self.splitter.addWidget(self.frame)

        self.horizontalLayout.addWidget(self.splitter)

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
        self.toolBar.addAction(self.actionOpenLogFile)
        self.toolBar.addAction(self.actionOpenProcessedDB)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHelp)

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
        self.actionEditTask.setToolTip(QCoreApplication.translate("MainWindow", u"Edit the selected task's property", None))
#endif // QT_CONFIG(tooltip)
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", u"Help", None))
#if QT_CONFIG(tooltip)
        self.actionHelp.setToolTip(QCoreApplication.translate("MainWindow", u"Help", None))
#endif // QT_CONFIG(tooltip)
        self.actionDeleteTask.setText(QCoreApplication.translate("MainWindow", u"DeleteTask", None))
#if QT_CONFIG(tooltip)
        self.actionDeleteTask.setToolTip(QCoreApplication.translate("MainWindow", u"Delete the selected task", None))
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
#if QT_CONFIG(tooltip)
        self.actionCopyTask.setToolTip(QCoreApplication.translate("MainWindow", u"Copy selected task", None))
#endif // QT_CONFIG(tooltip)
        self.actionStopTask.setText(QCoreApplication.translate("MainWindow", u"StopTask", None))
#if QT_CONFIG(tooltip)
        self.actionStopTask.setToolTip(QCoreApplication.translate("MainWindow", u"Stop the selected task", None))
#endif // QT_CONFIG(tooltip)
        self.actionStartTask.setText(QCoreApplication.translate("MainWindow", u"StartTask", None))
#if QT_CONFIG(tooltip)
        self.actionStartTask.setToolTip(QCoreApplication.translate("MainWindow", u"Start the selected task", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpenLogFile.setText(QCoreApplication.translate("MainWindow", u"LogFile", None))
#if QT_CONFIG(tooltip)
        self.actionOpenLogFile.setToolTip(QCoreApplication.translate("MainWindow", u"Open task's log file", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpenProcessedDB.setText(QCoreApplication.translate("MainWindow", u"ProcessedDB", None))
#if QT_CONFIG(tooltip)
        self.actionOpenProcessedDB.setToolTip(QCoreApplication.translate("MainWindow", u"Open task's processed db", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Task", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

