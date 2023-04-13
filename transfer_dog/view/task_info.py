#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/04 22:11:13

import logging, random

from PySide6 import QtCore
from PySide6.QtGui import QIcon, QFont, QStandardItem, QPainter, QPalette
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyledItemDelegate, QStyle, QStyleOption

from transfer_dog.utility.constants import *


class TaskInfoItem(QStandardItem):
    """表示在 QStandardItemModel 中的每一个 item 项"""
    def __init__(self, title: str = 'Task Title', description: str = 'Description...'):
        super(TaskInfoItem, self).__init__(title)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance. title[%s]', self.__class__.__name__, title)

        self.setData(title, role=QtCore.Qt.ItemDataRole.DisplayRole)

        self.widget = TaskInfoWidget(title, description)
        self.setData(self.widget, role=QtCore.Qt.ItemDataRole.UserRole)

        self.setEditable(False)
        pass

class TaskInfoWidget(QWidget):

    def __init__(self, title: str = 'Title', description: str = 'Description...', parent: QWidget = None):
        """Init a TaskInfoWidget instance.

        Args:
            title (str, optional): _description_. Defaults to 'Title'. Supports HTML syntax.
            description (str, optional): _description_. Defaults to 'Description...'. Supports HTML syntax.
        """

        super().__init__(parent)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self._option = None

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
        self.label_title.setText(title)  # QLabel.setText() 是支持富文本的
        # 但是富文本 QLabel 会吞噬鼠标事件，所以在此设置 label 对鼠标事件透明
        self.label_title.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # 3. description
        self.label_description = QLabel(self)
        self.label_description.setText(description)
        self.label_description.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
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

        # self.setAutoFillBackground(False)
        pass

    def paintEvent(self, event):
        """所有 QWidget 绘制的时候，都是调用 paintEvent() 方法进行绘制。

        1. 如果继承自某个内建 widget（比如 QLabel, QPushButton 这些），那么重写该方法将会覆盖父类的绘制行为。
        
        2. 此外！！！如果该 widget 还有 child widgets 的话，在执行完自己的 paintEvent() 之后，
        还会接着自动调用所有 child widgets 的 paintEvent()！
        （其实并不是所有，只需要调用与该 event.rect() 有交集的 child widgets 的 paintEvent() 方法。）

        3. 对于 TaskInfoWidget，我们本来不需要重写 paintEvent() 方法，只需由其 child widgets 自行绘制即可。

        4. 但是！如果想要让自定义的 QWidget 自己能够响应 StyleSheet 样式，就必须用如下代码重写 paintEvent()

        TODO: 可以给 wiget 设置一个状态为，比如 state = [RUNNING|WAITING|DISABLE]
        然后在 paintEvent 中根据这个状态位，设置 label_icon 的图标！

        Args:
            event (_type_): _description_
        """
        opt = QStyleOption()
        opt.initFrom(self)
        self.logger.debug('[%s] states: %s', self.label_title.text(), opt.state)
        
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
        pass


class TaskInfoDelegate(QStyledItemDelegate):
    def __init__(self, parent = None):
        super(TaskInfoDelegate, self).__init__(parent)
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance' % self.__class__.__name__)
        
        # 关闭 debug 输出
        # self.logger.setLevel(logging.INFO)
        pass

    def paint(self, painter, option, index):
        """如果重写 paint 方法，派生类就需要自己负责绘制所有内容，包括 文字、图标、背景色 等等。

        Args:
            painter (QtGui.QPainter): 画笔（建议在绘制前 painter.save 保存画笔状态，绘制后 painter.restore 恢复画笔状态）
            option (QtWidgets.QStyleOptionViewItem): 需要通过 initStyleOption() 方法初始化
            index (QtCore.QModelIndex): 待绘制 item 的 ModelIndex
        """
        assert index.isValid()
        
        # 1. 初始化 option （QStyleOptionViewItem 类型）
        self.initStyleOption(option, index)
        self.logger.debug('开始绘制 [%s], states: %s', index.data(), option.state)
        
        # 2. 判断是否是一级节点。如果是，则直接调用父类 paint 并返回
        if index.parent().isValid() == False:
            return super().paint(painter, option, index)
    
        # 3. 绘制二级节点背景
        tree_widget = option.widget
        tree_widget.style().drawPrimitive(QStyle.PrimitiveElement.PE_PanelItemViewItem, option, painter, tree_widget)

        # 4. 绘制二级节点
        task_widget = index.data(role=QtCore.Qt.ItemDataRole.UserRole)
        task_widget.setGeometry(option.rect)
        # 使用父节点自动绘制子节点的方式，不需要手工绘制

        # painter.save()
        # painter.translate(option.rect.topLeft())
        # task_widget.render(painter, QtCore.QPoint(0, 0), renderFlags=QWidget.RenderFlag.DrawChildren)
        # painter.restore()

        pass

    def sizeHint(self, option, index):
        """绘制自定义 widget 时，需要重写 sizeHint 来返回自定义 widget 的大小，来占位。 """
        # 如果是一级节点，返回父类的 sizeHint
        if index.parent().isValid() == False:
            self.logger.debug('一级节点: %s', index.data())
            return super().sizeHint(option, index)
        
        # 如果是二级节点，返回自定义 widget 的 sizeHint
        self.logger.debug('二级节点: %s', index.data())
        task_widget = index.data(role=QtCore.Qt.ItemDataRole.UserRole)
        return task_widget.sizeHint()


class TaskSearchProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance' % self.__class__.__name__)

        self.setRecursiveFilteringEnabled(True)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        pass

    
    def filterAcceptsRow(self, sourceRow: int, sourceParent: QtCore.QModelIndex) -> bool:
        """重写父类方法，判断节点是否满足过滤条件。
        节点可以通过 sourceParent[sourceRow] 定位，注意实参都是 sourceModel 的节点。
        过滤条件可以从 QSortFilterProxyModel.filterRegularExpression 属性获取
        
        注意 QSortFilterProxyModel 的默认匹配逻辑：
        只要父节点匹配成功，就会再递归判断其子节点。
        如果父节点匹配失败，且 recursiveFilteringEnabled=False, 则不再递归其子节点。
        如果父节点匹配失败，且 recursiveFilteringEnabled=True, 仍需递归判断其子节点。

        Args:
            sourceRow (int): 节点在父节点的第几行
            sourceParent (QtCore.QModelIndex): 父节点

        Returns:
            bool: 满足过滤条件返回 True, 否则返回 False
        """

        idx = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = self.sourceModel().itemFromIndex(idx)
        text = idx.data(role=self.filterRole())
        self.logger.debug('准备判断表达式(%s)是否匹配 [%s]', self.filterRegularExpression().pattern(), text)

        # 如果匹配表达式为空字符串，直接返回 True
        if self.filterRegularExpression().pattern() == '' or not self.filterRegularExpression().isValid():
            if type(item) is TaskInfoItem:
                item.widget.label_title.setText(text)
                item.widget.show()
            if not self.filterRegularExpression().isValid():
                self.logger.debug('表达式(%s)不合规', self.filterRegularExpression().pattern())
            return True
        
        # 使用匹配表达式对 text 进行匹配测试
        match_result = self.filterRegularExpression().match(text)
        if match_result.hasMatch():
            self.logger.debug('匹配 [%s]: %s', text, match_result)
            if type(item) is TaskInfoItem:
                captured = self.filterRegularExpression().match(text).captured()
                self.logger.debug('captured substring: %s', captured)
                display_text = '<span style="color:red;">{}</span>'.format(captured).join(text.split(captured)) if captured != '' else text
                item.widget.label_title.setText(display_text)
                item.widget.show()
            return True
        else:
            self.logger.debug('不匹配 [%s]', text)
            if type(item) is TaskInfoItem:
                item.widget.hide()
            return False
    