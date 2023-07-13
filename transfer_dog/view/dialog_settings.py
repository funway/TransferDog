#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/07/10 15:38:53

if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append( str(Path(__file__).parent.parent.parent) )
    pass

import logging
from pathlib import Path

from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QTranslator, QEvent

from transfer_dog.ui.ui_dialog_settings import Ui_Dialog
from transfer_dog.utility.constants import *
import transfer_dog.utility.global_variables as gv


class DialogSettings(QDialog, Ui_Dialog):
    """docstring for DialogSettings."""
    def __init__(self):
        super(DialogSettings, self).__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.setupUi()

        self.comb_language.currentIndexChanged.connect(self._on_change_language)
        self.comb_theme.currentIndexChanged.connect(self._on_change_theme)
        pass

    def setupUi(self):
        super().setupUi(self)

        # 语言
        langs = [f for f in LANGS_PATH.glob('*.qm')]
        langs.sort()
        for lang in langs:
            self.comb_language.addItem(lang.stem, str(lang))
        self.comb_language.setCurrentIndex(self.comb_language.findText(gv.cfg['DEFAULT']['lang']))

        # 主题
        themes = [f for f in RESOURCE_PATH.joinpath('qss').glob('*.qss')]
        themes.sort()
        for theme in themes:
            self.comb_theme.addItem(theme.stem, str(theme))
        self.comb_theme.setCurrentIndex(self.comb_theme.findText(gv.cfg['DEFAULT']['theme']))
        pass

    def closeEvent(self, event):
        self.logger.debug('关闭窗口，保存设置')
        with open(APP_CONFIG, 'w') as config_file:
            gv.cfg.write(config_file)
        pass

    def reject(self):
        self.close()
        super().reject()
        pass
    
    def _on_change_language(self):
        self.logger.debug('变更语言: %s, %s.', self.comb_language.currentText(), self.comb_language.currentData())
        
        if gv.translator is None:
            gv.translator = QTranslator()
            QApplication.installTranslator(gv.translator)

        gv.translator.load(self.comb_language.currentData())
        gv.cfg['DEFAULT']['lang'] = self.comb_language.currentText()
        pass

    def _on_change_theme(self):
        self.logger.debug('变更主题:  %s, %s.', self.comb_theme.currentText(), self.comb_theme.currentData())
        
        qss_file = self.comb_theme.currentData()
        try:
            with open(qss_file, 'r', encoding='UTF8') as qf:
                qss = qf.read()
                QApplication.instance().setStyleSheet(qss)
            gv.cfg['DEFAULT']['theme'] = self.comb_theme.currentText()
        except Exception as e:
            logging.exception('Load qss file failed! [%s]', qss_file)
        pass

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslateUi(self)

        super().changeEvent(event)
        pass

    def retranslateUi(self, Dialog):
        super().retranslateUi(Dialog)
        
        self.setWindowTitle(self.tr('Settings'))
        pass


def test(arg=None):
    import sys
    from PySide6.QtWidgets import QApplication

    logging_format = '%(asctime)s %(levelname)5s %(name)s.%(funcName)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

    app = QApplication(sys.argv)
    dialog = DialogSettings()
    ret = dialog.exec()
    logging.debug('窗口退出: %s', ret)

    pass


if __name__ == "__main__":
    test()

    