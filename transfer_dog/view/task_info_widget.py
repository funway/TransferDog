#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/31 23:17:48

import logging, random

from PySide6 import QtCore
from PySide6.QtGui import QIcon, QMovie, QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from transfer_dog.utility.constants import *

class TaskInfoWidget(QWidget):

    def __init__(self, title: str ='Title', description: str = 'Description...'):
        """Init a TaskInfoWidget instance.

        Args:
            title (str, optional): _description_. Defaults to 'Title'. Supports HTML syntax.
            description (str, optional): _description_. Defaults to 'Description...'. Supports HTML syntax.
        """

        super(TaskInfoWidget, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        # 1. 图标
        self.label_icon = QLabel(self)
        self.label_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_icon.setFixedWidth(40)

        # 1.1 QLabel 加载图片
        ## 使用 QIcon 来获得缩放后的 QPixmap
        self.label_icon.setPixmap(QIcon( str(RESOURCE_PATH / "img/dog.png") ).pixmap(32, 32))

        # 2. title
        self.label_title = QLabel(self)
        font = QFont()
        font.setPointSize(24)
        self.label_title.setFont(font)
        self.label_title.setText(title) # QLabel.setText() 是支持富文本的

        # 3. description
        self.label_description = QLabel(self)
        self.label_description.setText(description)
        
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.label_title)
        self.verticalLayout.addWidget(self.label_description)

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.label_icon)
        self.horizontalLayout.addLayout(self.verticalLayout)

        # self.label_icon.setStyleSheet('background-color: #{:06x}'.format(random.randint(0, 0xFFFFFF)))
        # self.label_title.setStyleSheet('background-color: #{:06x}'.format(random.randint(0, 0xFFFFFF)))
        # self.label_description.setStyleSheet('background-color: #{:06x}'.format(random.randint(0, 0xFFFFFF)))
        
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        pass
    