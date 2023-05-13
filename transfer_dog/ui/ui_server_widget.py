# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'server_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(497, 293)
        Form.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.hlayout_protocol = QHBoxLayout()
        self.hlayout_protocol.setObjectName(u"hlayout_protocol")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.hlayout_protocol.addWidget(self.label)

        self.rb_local = QRadioButton(Form)
        self.btn_group_protocol = QButtonGroup(Form)
        self.btn_group_protocol.setObjectName(u"btn_group_protocol")
        self.btn_group_protocol.addButton(self.rb_local)
        self.rb_local.setObjectName(u"rb_local")

        self.hlayout_protocol.addWidget(self.rb_local)

        self.rb_ftp = QRadioButton(Form)
        self.btn_group_protocol.addButton(self.rb_ftp)
        self.rb_ftp.setObjectName(u"rb_ftp")

        self.hlayout_protocol.addWidget(self.rb_ftp)

        self.rb_sftp = QRadioButton(Form)
        self.btn_group_protocol.addButton(self.rb_sftp)
        self.rb_sftp.setObjectName(u"rb_sftp")

        self.hlayout_protocol.addWidget(self.rb_sftp)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlayout_protocol.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.hlayout_protocol)

        self.gbox_server = QGroupBox(Form)
        self.gbox_server.setObjectName(u"gbox_server")
        self.verticalLayout_3 = QVBoxLayout(self.gbox_server)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.le_user = QLineEdit(self.gbox_server)
        self.le_user.setObjectName(u"le_user")

        self.gridLayout.addWidget(self.le_user, 1, 1, 1, 1)

        self.le_host = QLineEdit(self.gbox_server)
        self.le_host.setObjectName(u"le_host")

        self.gridLayout.addWidget(self.le_host, 0, 1, 1, 1)

        self.label_password = QLabel(self.gbox_server)
        self.label_password.setObjectName(u"label_password")
        self.label_password.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_password, 1, 2, 1, 1)

        self.le_port = QLineEdit(self.gbox_server)
        self.le_port.setObjectName(u"le_port")

        self.gridLayout.addWidget(self.le_port, 0, 3, 1, 1)

        self.le_password = QLineEdit(self.gbox_server)
        self.le_password.setObjectName(u"le_password")

        self.gridLayout.addWidget(self.le_password, 1, 3, 1, 1)

        self.label_2 = QLabel(self.gbox_server)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_6 = QLabel(self.gbox_server)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_5 = QLabel(self.gbox_server)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_encoding = QLabel(self.gbox_server)
        self.label_encoding.setObjectName(u"label_encoding")
        self.label_encoding.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_encoding)

        self.comb_encoding = QComboBox(self.gbox_server)
        self.comb_encoding.addItem("")
        self.comb_encoding.addItem("")
        self.comb_encoding.setObjectName(u"comb_encoding")
        self.comb_encoding.setEditable(True)

        self.horizontalLayout_3.addWidget(self.comb_encoding)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.stackedWidget = QStackedWidget(self.gbox_server)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_ftp = QWidget()
        self.page_ftp.setObjectName(u"page_ftp")
        self.verticalLayout_4 = QVBoxLayout(self.page_ftp)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.chkb_passive = QCheckBox(self.page_ftp)
        self.chkb_passive.setObjectName(u"chkb_passive")

        self.horizontalLayout.addWidget(self.chkb_passive)

        self.chkb_ftps = QCheckBox(self.page_ftp)
        self.chkb_ftps.setObjectName(u"chkb_ftps")

        self.horizontalLayout.addWidget(self.chkb_ftps)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.stackedWidget.addWidget(self.page_ftp)
        self.page_sftp = QWidget()
        self.page_sftp.setObjectName(u"page_sftp")
        self.verticalLayout_2 = QVBoxLayout(self.page_sftp)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.chkb_use_keyfile = QCheckBox(self.page_sftp)
        self.chkb_use_keyfile.setObjectName(u"chkb_use_keyfile")

        self.horizontalLayout_2.addWidget(self.chkb_use_keyfile)

        self.le_keyfile = QLineEdit(self.page_sftp)
        self.le_keyfile.setObjectName(u"le_keyfile")
        self.le_keyfile.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.le_keyfile)

        self.pb_keyfile = QPushButton(self.page_sftp)
        self.pb_keyfile.setObjectName(u"pb_keyfile")
        self.pb_keyfile.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pb_keyfile)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.stackedWidget.addWidget(self.page_sftp)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.gbox_server)

        self.hlayout_dir = QHBoxLayout()
        self.hlayout_dir.setObjectName(u"hlayout_dir")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.hlayout_dir.addWidget(self.label_4)

        self.le_dir = QLineEdit(Form)
        self.le_dir.setObjectName(u"le_dir")

        self.hlayout_dir.addWidget(self.le_dir)

        self.pb_dir = QPushButton(Form)
        self.pb_dir.setObjectName(u"pb_dir")

        self.hlayout_dir.addWidget(self.pb_dir)


        self.verticalLayout.addLayout(self.hlayout_dir)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.rb_local, self.rb_ftp)
        QWidget.setTabOrder(self.rb_ftp, self.rb_sftp)
        QWidget.setTabOrder(self.rb_sftp, self.le_host)
        QWidget.setTabOrder(self.le_host, self.le_port)
        QWidget.setTabOrder(self.le_port, self.le_user)
        QWidget.setTabOrder(self.le_user, self.le_password)
        QWidget.setTabOrder(self.le_password, self.le_dir)
        QWidget.setTabOrder(self.le_dir, self.pb_dir)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Protocol", None))
        self.rb_local.setText(QCoreApplication.translate("Form", u"Local", None))
        self.rb_ftp.setText(QCoreApplication.translate("Form", u"FTP(S)", None))
        self.rb_sftp.setText(QCoreApplication.translate("Form", u"SFTP", None))
        self.gbox_server.setTitle(QCoreApplication.translate("Form", u"Server", None))
        self.label_password.setText(QCoreApplication.translate("Form", u"Password", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Host", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"User", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Port", None))
        self.label_encoding.setText(QCoreApplication.translate("Form", u"Encoding", None))
        self.comb_encoding.setItemText(0, QCoreApplication.translate("Form", u"UTF8", None))
        self.comb_encoding.setItemText(1, QCoreApplication.translate("Form", u"GB2312", None))

        self.chkb_passive.setText(QCoreApplication.translate("Form", u"Passive Mode", None))
        self.chkb_ftps.setText(QCoreApplication.translate("Form", u"FTP over TLS", None))
        self.chkb_use_keyfile.setText(QCoreApplication.translate("Form", u"Key File", None))
        self.pb_keyfile.setText(QCoreApplication.translate("Form", u"Browse", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Directory", None))
        self.pb_dir.setText(QCoreApplication.translate("Form", u"Browse", None))
    # retranslateUi

