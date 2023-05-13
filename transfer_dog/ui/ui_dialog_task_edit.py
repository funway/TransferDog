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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(650, 663)
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
"}\n"
"\n"
"QScrollArea {\n"
"	border: none;\n"
"}")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 626, 597))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gbox_general = QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_general.setObjectName(u"gbox_general")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbox_general.sizePolicy().hasHeightForWidth())
        self.gbox_general.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.gbox_general)
        self.gridLayout.setObjectName(u"gridLayout")
        self.chkb_task_enabled = QCheckBox(self.gbox_general)
        self.chkb_task_enabled.setObjectName(u"chkb_task_enabled")

        self.gridLayout.addWidget(self.chkb_task_enabled, 1, 2, 1, 1)

        self.le_task_schedule = QLineEdit(self.gbox_general)
        self.le_task_schedule.setObjectName(u"le_task_schedule")

        self.gridLayout.addWidget(self.le_task_schedule, 1, 1, 1, 1)

        self.label_2 = QLabel(self.gbox_general)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.le_task_name = QLineEdit(self.gbox_general)
        self.le_task_name.setObjectName(u"le_task_name")

        self.gridLayout.addWidget(self.le_task_name, 0, 1, 1, 1)

        self.label = QLabel(self.gbox_general)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.gbox_general)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.comb_task_group = QComboBox(self.gbox_general)
        self.comb_task_group.setObjectName(u"comb_task_group")
        self.comb_task_group.setEditable(True)

        self.gridLayout.addWidget(self.comb_task_group, 0, 3, 1, 1)


        self.verticalLayout_3.addWidget(self.gbox_general)

        self.gbox_source = QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_source.setObjectName(u"gbox_source")
        self.verticalLayout_2 = QVBoxLayout(self.gbox_source)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.gbox_source)

        self.gbox_filter = QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_filter.setObjectName(u"gbox_filter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gbox_filter.sizePolicy().hasHeightForWidth())
        self.gbox_filter.setSizePolicy(sizePolicy1)
        self.verticalLayout_5 = QVBoxLayout(self.gbox_filter)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.label_8 = QLabel(self.gbox_filter)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_2.addWidget(self.label_8)

        self.le_filter_filename = QLineEdit(self.gbox_filter)
        self.le_filter_filename.setObjectName(u"le_filter_filename")

        self.horizontalLayout_2.addWidget(self.le_filter_filename)

        self.pb_regex_test = QPushButton(self.gbox_filter)
        self.pb_regex_test.setObjectName(u"pb_regex_test")

        self.horizontalLayout_2.addWidget(self.pb_regex_test)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(3)
        self.gridLayout_2.setVerticalSpacing(12)
        self.le_processed_reserve = QLineEdit(self.gbox_filter)
        self.le_processed_reserve.setObjectName(u"le_processed_reserve")

        self.gridLayout_2.addWidget(self.le_processed_reserve, 2, 4, 1, 1)

        self.label_12 = QLabel(self.gbox_filter)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_12, 1, 3, 1, 1)

        self.le_middleware_arg = QLineEdit(self.gbox_filter)
        self.le_middleware_arg.setObjectName(u"le_middleware_arg")

        self.gridLayout_2.addWidget(self.le_middleware_arg, 1, 4, 1, 1)

        self.label_11 = QLabel(self.gbox_filter)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 1, 0, 1, 1)

        self.spinBox_subdir_recursion = QSpinBox(self.gbox_filter)
        self.spinBox_subdir_recursion.setObjectName(u"spinBox_subdir_recursion")
        self.spinBox_subdir_recursion.setMaximum(999)

        self.gridLayout_2.addWidget(self.spinBox_subdir_recursion, 0, 4, 1, 1)

        self.label_4 = QLabel(self.gbox_filter)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_9 = QLabel(self.gbox_filter)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)

        self.comb_filter_valid_time = QComboBox(self.gbox_filter)
        self.comb_filter_valid_time.setObjectName(u"comb_filter_valid_time")

        self.gridLayout_2.addWidget(self.comb_filter_valid_time, 0, 1, 1, 1)

        self.comb_middleware = QComboBox(self.gbox_filter)
        self.comb_middleware.setObjectName(u"comb_middleware")

        self.gridLayout_2.addWidget(self.comb_middleware, 1, 1, 1, 1)

        self.le_suffix = QLineEdit(self.gbox_filter)
        self.le_suffix.setObjectName(u"le_suffix")

        self.gridLayout_2.addWidget(self.le_suffix, 2, 1, 1, 1)

        self.label_10 = QLabel(self.gbox_filter)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 0, 3, 1, 1)

        self.label_5 = QLabel(self.gbox_filter)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 2, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 8, -1, -1)
        self.chkb_delete_source = QCheckBox(self.gbox_filter)
        self.chkb_delete_source.setObjectName(u"chkb_delete_source")

        self.horizontalLayout_3.addWidget(self.chkb_delete_source)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.gbox_filter)

        self.gbox_dest = QGroupBox(self.scrollAreaWidgetContents)
        self.gbox_dest.setObjectName(u"gbox_dest")
        self.verticalLayout_4 = QVBoxLayout(self.gbox_dest)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, -1, 0)

        self.verticalLayout_3.addWidget(self.gbox_dest)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_error_msg = QLabel(Dialog)
        self.label_error_msg.setObjectName(u"label_error_msg")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_error_msg.sizePolicy().hasHeightForWidth())
        self.label_error_msg.setSizePolicy(sizePolicy2)
        self.label_error_msg.setWordWrap(False)

        self.horizontalLayout.addWidget(self.label_error_msg)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy3)
        self.buttonBox.setMaximumSize(QSize(16777215, 16777215))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.gbox_general.setTitle(QCoreApplication.translate("Dialog", u"General", None))
        self.chkb_task_enabled.setText(QCoreApplication.translate("Dialog", u"Enable", None))
        self.le_task_schedule.setPlaceholderText(QCoreApplication.translate("Dialog", u"* * * * *", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Task Group", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Task Name", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Schedule", None))
        self.gbox_source.setTitle(QCoreApplication.translate("Dialog", u"Source", None))
        self.gbox_filter.setTitle(QCoreApplication.translate("Dialog", u"Filter / Middleware", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Filename RegEx", None))
        self.le_filter_filename.setText(QCoreApplication.translate("Dialog", u".*", None))
        self.pb_regex_test.setText(QCoreApplication.translate("Dialog", u"Test", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Middleware Argument", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Middleware", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Temp Suffix", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Valid Time", None))
        self.le_suffix.setPlaceholderText(QCoreApplication.translate("Dialog", u".tmp", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Subdir Recursion", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Processed History", None))
        self.chkb_delete_source.setText(QCoreApplication.translate("Dialog", u"Delete Source", None))
        self.gbox_dest.setTitle(QCoreApplication.translate("Dialog", u"Destination", None))
        self.label_error_msg.setText("")
    # retranslateUi

