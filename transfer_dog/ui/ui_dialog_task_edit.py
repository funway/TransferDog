# Form implementation generated from reading ui file '/Users/funway/project/python/TransferDog/transfer_dog/ui/dialog_task_edit.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 692)
        Dialog.setStyleSheet("QGroupBox {\n"
"    font: bold;\n"
"    border: 1px solid silver;\n"
"    border-radius: 6px;\n"
"    margin-top: 6px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 7px;\n"
"    padding: 0px 5px 0px 5px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 3, 2, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_3, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_5)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 3, 3, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 0, 1, 1, 3)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_2.addWidget(self.lineEdit_4)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_3.addWidget(self.checkBox_3, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(164, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 3, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_3.addWidget(self.checkBox_4, 1, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_3.addWidget(self.lineEdit_5, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_5.addWidget(self.label_16)
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_5.setObjectName("radioButton_5")
        self.horizontalLayout_5.addWidget(self.radioButton_5)
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_6.setObjectName("radioButton_6")
        self.horizontalLayout_5.addWidget(self.radioButton_6)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_14 = QtWidgets.QLabel(self.groupBox_6)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 3, 0, 1, 1)
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox_6.setChecked(True)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout_5.addWidget(self.checkBox_6, 3, 2, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.gridLayout_5.addWidget(self.comboBox_5, 3, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_6)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 0, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_5.addItem(spacerItem5, 3, 3, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout_5.addWidget(self.lineEdit_8, 0, 1, 1, 3)
        self.verticalLayout_4.addWidget(self.groupBox_6)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_17 = QtWidgets.QLabel(self.groupBox_4)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_6.addWidget(self.label_17)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.horizontalLayout_6.addWidget(self.lineEdit_9)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_6.addWidget(self.pushButton_4)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "General"))
        self.label.setText(_translate("Dialog", "Task Name"))
        self.label_2.setText(_translate("Dialog", "Task Group"))
        self.label_3.setText(_translate("Dialog", "Schedule"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "* * * * *"))
        self.checkBox.setText(_translate("Dialog", "Enable"))
        self.groupBox_2.setTitle(_translate("Dialog", "Source"))
        self.label_4.setText(_translate("Dialog", "Protocol"))
        self.radioButton.setText(_translate("Dialog", "Local"))
        self.radioButton_2.setText(_translate("Dialog", "FTP"))
        self.groupBox_5.setTitle(_translate("Dialog", "Server"))
        self.label_6.setText(_translate("Dialog", "Encoding"))
        self.checkBox_2.setText(_translate("Dialog", "Passive Mode"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "UTF8"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "GB2312"))
        self.label_5.setText(_translate("Dialog", "Address"))
        self.lineEdit_3.setPlaceholderText(_translate("Dialog", "username:password@host:port"))
        self.label_7.setText(_translate("Dialog", "Directory"))
        self.pushButton.setText(_translate("Dialog", "Browse"))
        self.groupBox_3.setTitle(_translate("Dialog", "Filter / Middleware"))
        self.pushButton_2.setText(_translate("Dialog", "Test"))
        self.checkBox_3.setText(_translate("Dialog", "Scan Subdirectories"))
        self.checkBox_4.setText(_translate("Dialog", "Delete Source"))
        self.label_9.setText(_translate("Dialog", "Valid Time"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "All Time"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "10 Minutes"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "30 Minutes"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "1 Hour"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "3 Hours"))
        self.comboBox_2.setItemText(5, _translate("Dialog", "12 Hours"))
        self.label_8.setText(_translate("Dialog", "Filename RegEx"))
        self.groupBox_4.setTitle(_translate("Dialog", "Destination"))
        self.label_16.setText(_translate("Dialog", "Protocol"))
        self.radioButton_5.setText(_translate("Dialog", "Local"))
        self.radioButton_6.setText(_translate("Dialog", "FTP"))
        self.groupBox_6.setTitle(_translate("Dialog", "Server"))
        self.label_14.setText(_translate("Dialog", "Encoding"))
        self.checkBox_6.setText(_translate("Dialog", "Passive Mode"))
        self.comboBox_5.setItemText(0, _translate("Dialog", "UTF8"))
        self.comboBox_5.setItemText(1, _translate("Dialog", "GB2312"))
        self.label_15.setText(_translate("Dialog", "Address"))
        self.lineEdit_8.setPlaceholderText(_translate("Dialog", "username:password@host:port"))
        self.label_17.setText(_translate("Dialog", "Directory"))
        self.pushButton_4.setText(_translate("Dialog", "Browse"))
