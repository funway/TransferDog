#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/09 09:56:08

if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append( str(Path(__file__).parent.parent.parent) )
    pass

import logging, re

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QRegularExpression

from transfer_dog.ui.ui_dialog_regular_express import Ui_Dialog

class DialogRegularExpress(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.setupUi(self)

        default_inputs = 'ceshi\n' \
                    '任务组ab\n' \
                    'task_发送任务\n' \
                    '收集+分发\n' \
                    '08/12/1985\n' \
                    '166test'
        self.pte_input.setPlainText(default_inputs)

        self.pushButton.clicked.connect(self._start_match)

        pass

    def _start_match(self):
        self.logger.debug('start match')
        self.pte_output.appendPlainText('=== start match =========================================')

        pattern = self.lineEdit.text().strip()
        q_reg = QRegularExpression(pattern, options=QRegularExpression.PatternOption.CaseInsensitiveOption)
        p_reg = re.compile(pattern, flags=re.IGNORECASE)

        for row in self.pte_input.toPlainText().splitlines():
            self.pte_output.appendPlainText('开始匹配使用 (%s) 匹配 [%s]' % (pattern, row))

            match_result = q_reg.match(row)
            self.pte_output.appendPlainText(str(match_result))
            self.pte_output.appendPlainText('QRegularExpression captured: %s' % match_result.captured())
            
            p_result = p_reg.search(row)
            self.pte_output.appendPlainText(str(p_result))
            self.pte_output.appendPlainText('Python re searched: %s' % p_result[0] if p_result else 'None')

            self.pte_output.appendPlainText('============================')
            pass
        pass
    

def test(arg=None):
    import sys
    from PySide6.QtWidgets import QApplication

    logging_format = '%(asctime)s %(levelname)5s %(name)s.%(funcName)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

    app = QApplication(sys.argv)
    dialog = DialogRegularExpress()
    ret = dialog.exec()
    logging.info('窗口退出: %s', ret)

    pass


if __name__ == "__main__":
    test()