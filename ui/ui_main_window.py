# Form implementation generated from reading ui file '/Users/funway/project/python/TransferDog/ui/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("QToolBar {\n"
"    /* set style for QToolBar */\n"
"}\n"
"QToolBar QToolButton {\n"
"    /* set style for QToolButtons in QToolBar */\n"
"    font-size: 15px;\n"
"}\n"
"QToolBar QToolButton:hover {\n"
"    border-radius: 5px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fdfbf7, stop: 1 #cfccc7);\n"
"}\n"
"QToolBar QToolButton:pressed {\n"
"    /* background-color: blue; */\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionNewTask = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/Users/funway/project/python/TransferDog/ui/resources/icons/add.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionNewTask.setIcon(icon)
        self.actionNewTask.setObjectName("actionNewTask")
        self.actionEditTask = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("/Users/funway/project/python/TransferDog/ui/resources/icons/list.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionEditTask.setIcon(icon1)
        self.actionEditTask.setObjectName("actionEditTask")
        self.actionTest = QtGui.QAction(MainWindow)
        self.actionTest.setObjectName("actionTest")
        self.toolBar.addAction(self.actionNewTask)
        self.toolBar.addAction(self.actionEditTask)
        self.toolBar.addAction(self.actionTest)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNewTask.setText(_translate("MainWindow", "NewTask"))
        self.actionNewTask.setToolTip(_translate("MainWindow", "Add new transfer task"))
        self.actionEditTask.setText(_translate("MainWindow", "EditTask"))
        self.actionEditTask.setToolTip(_translate("MainWindow", "Edit a task\'s property"))
        self.actionTest.setText(_translate("MainWindow", "Test"))
