# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_regular_express.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(557, 476)
        Dialog.setStyleSheet(u"")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.le_regex = QLineEdit(Dialog)
        self.le_regex.setObjectName(u"le_regex")

        self.horizontalLayout.addWidget(self.le_regex)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.text_output = QTextBrowser(Dialog)
        self.text_output.setObjectName(u"text_output")

        self.gridLayout.addWidget(self.text_output, 2, 1, 1, 1)

        self.text_input = QPlainTextEdit(Dialog)
        self.text_input.setObjectName(u"text_input")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_input.sizePolicy().hasHeightForWidth())
        self.text_input.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.text_input, 0, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"start", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Input", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"RegEx", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Output", None))
        self.text_input.setPlainText("")
        self.text_input.setPlaceholderText(QCoreApplication.translate("Dialog", u"Input some filenames for testing.", None))
    # retranslateUi

