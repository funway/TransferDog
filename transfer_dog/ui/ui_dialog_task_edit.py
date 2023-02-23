# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_task_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(650, 704)
        Dialog.setStyleSheet(u"QGroupBox {\n"
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
"}\n"
"\n"
"QLabel#label_error_msg {\n"
"	color: red;\n"
"}")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_task_enabled = QCheckBox(self.groupBox)
        self.checkBox_task_enabled.setObjectName(u"checkBox_task_enabled")

        self.gridLayout.addWidget(self.checkBox_task_enabled, 1, 2, 1, 1)

        self.lineEdit_task_schedule = QLineEdit(self.groupBox)
        self.lineEdit_task_schedule.setObjectName(u"lineEdit_task_schedule")

        self.gridLayout.addWidget(self.lineEdit_task_schedule, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.lineEdit_task_name = QLineEdit(self.groupBox)
        self.lineEdit_task_name.setObjectName(u"lineEdit_task_name")

        self.gridLayout.addWidget(self.lineEdit_task_name, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.comboBox_task_group = QComboBox(self.groupBox)
        self.comboBox_task_group.setObjectName(u"comboBox_task_group")
        self.comboBox_task_group.setEditable(True)

        self.gridLayout.addWidget(self.comboBox_task_group, 0, 3, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.radioButton_src_local = QRadioButton(self.groupBox_2)
        self.buttonGroup_src_protocol = QButtonGroup(Dialog)
        self.buttonGroup_src_protocol.setObjectName(u"buttonGroup_src_protocol")
        self.buttonGroup_src_protocol.addButton(self.radioButton_src_local)
        self.radioButton_src_local.setObjectName(u"radioButton_src_local")
        self.radioButton_src_local.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton_src_local)

        self.radioButton_src_ftp = QRadioButton(self.groupBox_2)
        self.buttonGroup_src_protocol.addButton(self.radioButton_src_ftp)
        self.radioButton_src_ftp.setObjectName(u"radioButton_src_ftp")
        self.radioButton_src_ftp.setChecked(False)

        self.horizontalLayout.addWidget(self.radioButton_src_ftp)

        self.radioButton_src_sftp = QRadioButton(self.groupBox_2)
        self.buttonGroup_src_protocol.addButton(self.radioButton_src_sftp)
        self.radioButton_src_sftp.setObjectName(u"radioButton_src_sftp")

        self.horizontalLayout.addWidget(self.radioButton_src_sftp)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.groupBox_src_server = QGroupBox(self.groupBox_2)
        self.groupBox_src_server.setObjectName(u"groupBox_src_server")
        self.groupBox_src_server.setEnabled(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_src_server)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.groupBox_src_server)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)

        self.checkBox_src_server_passive = QCheckBox(self.groupBox_src_server)
        self.checkBox_src_server_passive.setObjectName(u"checkBox_src_server_passive")
        self.checkBox_src_server_passive.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_src_server_passive, 3, 2, 1, 1)

        self.comboBox_src_server_encoding = QComboBox(self.groupBox_src_server)
        self.comboBox_src_server_encoding.addItem("")
        self.comboBox_src_server_encoding.addItem("")
        self.comboBox_src_server_encoding.setObjectName(u"comboBox_src_server_encoding")

        self.gridLayout_2.addWidget(self.comboBox_src_server_encoding, 3, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_src_server)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 3, 3, 1, 1)

        self.lineEdit_src_server_address = QLineEdit(self.groupBox_src_server)
        self.lineEdit_src_server_address.setObjectName(u"lineEdit_src_server_address")

        self.gridLayout_2.addWidget(self.lineEdit_src_server_address, 0, 1, 1, 3)


        self.verticalLayout_2.addWidget(self.groupBox_src_server)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.lineEdit_src_dir = QLineEdit(self.groupBox_2)
        self.lineEdit_src_dir.setObjectName(u"lineEdit_src_dir")

        self.horizontalLayout_2.addWidget(self.lineEdit_src_dir)

        self.pushButton_src_browse = QPushButton(self.groupBox_2)
        self.pushButton_src_browse.setObjectName(u"pushButton_src_browse")

        self.horizontalLayout_2.addWidget(self.pushButton_src_browse)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_2 = QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_3.addWidget(self.pushButton_2, 0, 2, 1, 1)

        self.checkBox_scan_subdir = QCheckBox(self.groupBox_3)
        self.checkBox_scan_subdir.setObjectName(u"checkBox_scan_subdir")

        self.gridLayout_3.addWidget(self.checkBox_scan_subdir, 1, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(164, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)

        self.checkBox_delete_source = QCheckBox(self.groupBox_3)
        self.checkBox_delete_source.setObjectName(u"checkBox_delete_source")

        self.gridLayout_3.addWidget(self.checkBox_delete_source, 1, 3, 1, 1)

        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)

        self.comboBox_filter_valid_time = QComboBox(self.groupBox_3)
        self.comboBox_filter_valid_time.setObjectName(u"comboBox_filter_valid_time")

        self.gridLayout_3.addWidget(self.comboBox_filter_valid_time, 1, 1, 1, 1)

        self.lineEdit_filter_filename = QLineEdit(self.groupBox_3)
        self.lineEdit_filter_filename.setObjectName(u"lineEdit_filter_filename")

        self.gridLayout_3.addWidget(self.lineEdit_filter_filename, 0, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(Dialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_16 = QLabel(self.groupBox_4)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_5.addWidget(self.label_16)

        self.radioButton_dest_local = QRadioButton(self.groupBox_4)
        self.buttonGroup_dest_protocol = QButtonGroup(Dialog)
        self.buttonGroup_dest_protocol.setObjectName(u"buttonGroup_dest_protocol")
        self.buttonGroup_dest_protocol.addButton(self.radioButton_dest_local)
        self.radioButton_dest_local.setObjectName(u"radioButton_dest_local")
        self.radioButton_dest_local.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radioButton_dest_local)

        self.radioButton_dest_ftp = QRadioButton(self.groupBox_4)
        self.buttonGroup_dest_protocol.addButton(self.radioButton_dest_ftp)
        self.radioButton_dest_ftp.setObjectName(u"radioButton_dest_ftp")

        self.horizontalLayout_5.addWidget(self.radioButton_dest_ftp)

        self.radioButton_dest_sftp = QRadioButton(self.groupBox_4)
        self.buttonGroup_dest_protocol.addButton(self.radioButton_dest_sftp)
        self.radioButton_dest_sftp.setObjectName(u"radioButton_dest_sftp")

        self.horizontalLayout_5.addWidget(self.radioButton_dest_sftp)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.groupBox_dest_server = QGroupBox(self.groupBox_4)
        self.groupBox_dest_server.setObjectName(u"groupBox_dest_server")
        self.groupBox_dest_server.setEnabled(False)
        self.gridLayout_5 = QGridLayout(self.groupBox_dest_server)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_14 = QLabel(self.groupBox_dest_server)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_5.addWidget(self.label_14, 3, 0, 1, 1)

        self.checkBox_dest_server_passive = QCheckBox(self.groupBox_dest_server)
        self.checkBox_dest_server_passive.setObjectName(u"checkBox_dest_server_passive")
        self.checkBox_dest_server_passive.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_dest_server_passive, 3, 2, 1, 1)

        self.comboBox_dest_server_encoding = QComboBox(self.groupBox_dest_server)
        self.comboBox_dest_server_encoding.addItem("")
        self.comboBox_dest_server_encoding.addItem("")
        self.comboBox_dest_server_encoding.setObjectName(u"comboBox_dest_server_encoding")

        self.gridLayout_5.addWidget(self.comboBox_dest_server_encoding, 3, 1, 1, 1)

        self.label_15 = QLabel(self.groupBox_dest_server)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 3, 3, 1, 1)

        self.lineEdit_dest_server_address = QLineEdit(self.groupBox_dest_server)
        self.lineEdit_dest_server_address.setObjectName(u"lineEdit_dest_server_address")

        self.gridLayout_5.addWidget(self.lineEdit_dest_server_address, 0, 1, 1, 3)


        self.verticalLayout_4.addWidget(self.groupBox_dest_server)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_6.addWidget(self.label_17)

        self.lineEdit_dest_dir = QLineEdit(self.groupBox_4)
        self.lineEdit_dest_dir.setObjectName(u"lineEdit_dest_dir")

        self.horizontalLayout_6.addWidget(self.lineEdit_dest_dir)

        self.pushButton_dest_browse = QPushButton(self.groupBox_4)
        self.pushButton_dest_browse.setObjectName(u"pushButton_dest_browse")

        self.horizontalLayout_6.addWidget(self.pushButton_dest_browse)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_10)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 0, 0, 0)
        self.label_error_msg = QLabel(self.frame)
        self.label_error_msg.setObjectName(u"label_error_msg")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_error_msg.sizePolicy().hasHeightForWidth())
        self.label_error_msg.setSizePolicy(sizePolicy2)
        self.label_error_msg.setWordWrap(False)

        self.horizontalLayout_3.addWidget(self.label_error_msg)

        self.buttonBox = QDialogButtonBox(self.frame)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy3)
        self.buttonBox.setMaximumSize(QSize(16777215, 16777215))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_3.addWidget(self.buttonBox)


        self.verticalLayout.addWidget(self.frame)

        QWidget.setTabOrder(self.lineEdit_task_name, self.comboBox_task_group)
        QWidget.setTabOrder(self.comboBox_task_group, self.lineEdit_task_schedule)
        QWidget.setTabOrder(self.lineEdit_task_schedule, self.checkBox_task_enabled)
        QWidget.setTabOrder(self.checkBox_task_enabled, self.radioButton_src_local)
        QWidget.setTabOrder(self.radioButton_src_local, self.radioButton_src_ftp)
        QWidget.setTabOrder(self.radioButton_src_ftp, self.radioButton_src_sftp)
        QWidget.setTabOrder(self.radioButton_src_sftp, self.lineEdit_src_server_address)
        QWidget.setTabOrder(self.lineEdit_src_server_address, self.comboBox_src_server_encoding)
        QWidget.setTabOrder(self.comboBox_src_server_encoding, self.checkBox_src_server_passive)
        QWidget.setTabOrder(self.checkBox_src_server_passive, self.lineEdit_src_dir)
        QWidget.setTabOrder(self.lineEdit_src_dir, self.pushButton_src_browse)
        QWidget.setTabOrder(self.pushButton_src_browse, self.lineEdit_filter_filename)
        QWidget.setTabOrder(self.lineEdit_filter_filename, self.pushButton_2)
        QWidget.setTabOrder(self.pushButton_2, self.comboBox_filter_valid_time)
        QWidget.setTabOrder(self.comboBox_filter_valid_time, self.checkBox_scan_subdir)
        QWidget.setTabOrder(self.checkBox_scan_subdir, self.checkBox_delete_source)
        QWidget.setTabOrder(self.checkBox_delete_source, self.radioButton_dest_local)
        QWidget.setTabOrder(self.radioButton_dest_local, self.radioButton_dest_ftp)
        QWidget.setTabOrder(self.radioButton_dest_ftp, self.radioButton_dest_sftp)
        QWidget.setTabOrder(self.radioButton_dest_sftp, self.lineEdit_dest_server_address)
        QWidget.setTabOrder(self.lineEdit_dest_server_address, self.comboBox_dest_server_encoding)
        QWidget.setTabOrder(self.comboBox_dest_server_encoding, self.checkBox_dest_server_passive)
        QWidget.setTabOrder(self.checkBox_dest_server_passive, self.lineEdit_dest_dir)
        QWidget.setTabOrder(self.lineEdit_dest_dir, self.pushButton_dest_browse)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"General", None))
        self.checkBox_task_enabled.setText(QCoreApplication.translate("Dialog", u"Enable", None))
        self.lineEdit_task_schedule.setPlaceholderText(QCoreApplication.translate("Dialog", u"* * * * *", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Task Group", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Task Name", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Schedule", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Source", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Protocol", None))
        self.radioButton_src_local.setText(QCoreApplication.translate("Dialog", u"Local", None))
        self.radioButton_src_ftp.setText(QCoreApplication.translate("Dialog", u"FTP", None))
        self.radioButton_src_sftp.setText(QCoreApplication.translate("Dialog", u"SFTP", None))
        self.groupBox_src_server.setTitle(QCoreApplication.translate("Dialog", u"Server", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Encoding", None))
        self.checkBox_src_server_passive.setText(QCoreApplication.translate("Dialog", u"Passive Mode", None))
        self.comboBox_src_server_encoding.setItemText(0, QCoreApplication.translate("Dialog", u"UTF8", None))
        self.comboBox_src_server_encoding.setItemText(1, QCoreApplication.translate("Dialog", u"GB2312", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Address", None))
        self.lineEdit_src_server_address.setPlaceholderText(QCoreApplication.translate("Dialog", u"username:password@host:port", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Directory", None))
        self.pushButton_src_browse.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Filter / Middleware", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Test", None))
        self.checkBox_scan_subdir.setText(QCoreApplication.translate("Dialog", u"Scan Subdirectories", None))
        self.checkBox_delete_source.setText(QCoreApplication.translate("Dialog", u"Delete Source", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Valid Time", None))
        self.lineEdit_filter_filename.setText(QCoreApplication.translate("Dialog", u".*", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Filename RegEx", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Destination", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Protocol", None))
        self.radioButton_dest_local.setText(QCoreApplication.translate("Dialog", u"Local", None))
        self.radioButton_dest_ftp.setText(QCoreApplication.translate("Dialog", u"FTP", None))
        self.radioButton_dest_sftp.setText(QCoreApplication.translate("Dialog", u"SFTP", None))
        self.groupBox_dest_server.setTitle(QCoreApplication.translate("Dialog", u"Server", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Encoding", None))
        self.checkBox_dest_server_passive.setText(QCoreApplication.translate("Dialog", u"Passive Mode", None))
        self.comboBox_dest_server_encoding.setItemText(0, QCoreApplication.translate("Dialog", u"UTF8", None))
        self.comboBox_dest_server_encoding.setItemText(1, QCoreApplication.translate("Dialog", u"GB2312", None))

        self.label_15.setText(QCoreApplication.translate("Dialog", u"Address", None))
        self.lineEdit_dest_server_address.setPlaceholderText(QCoreApplication.translate("Dialog", u"username:password@host:port", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Directory", None))
        self.pushButton_dest_browse.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.label_error_msg.setText("")
    # retranslateUi

