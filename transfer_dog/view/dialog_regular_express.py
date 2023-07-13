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

    def __init__(self, regex: str = ''):
        super().__init__()

        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.setupUi(self)

        default_inputs = [
            'PJJ8DSLM.120',
            '123测试任务ab',
            r'C:\\ftproot\fy2g\202305\sat_20230512_if.png',
            '/data/radar/zggg_radar_ppip_202305201011.png'
        ]
        self.text_input.setPlainText('\n'.join(default_inputs))
        self.le_regex.setText(regex)
        self.setWindowTitle(self.tr('RegularExpression Test'))

        self.pushButton.clicked.connect(self._start_match)

        pass

    def _start_match(self):
        self.logger.debug('start match')
        self.text_output.clear()

        pattern = self.le_regex.text().strip()
        # q_reg = QRegularExpression(pattern, options=QRegularExpression.PatternOption.CaseInsensitiveOption)
        # p_reg = re.compile(pattern, flags=re.IGNORECASE)
        # 应该由输入的表达式来指定要不要忽略大小写，在正则表达式前头添加 (?i) 表示忽略大小写
        qt_reg = QRegularExpression(pattern)
        py_reg = re.compile(pattern)


        for row in self.text_input.toPlainText().splitlines():
            self.logger.debug('使用「%s」匹配 [%s]' % (pattern, row))

            qt_result = qt_reg.match(row)
            self.logger.debug('QRegularExpression match result: %s' % qt_result)
            self.logger.debug('QRegularExpression captured: %s' % qt_result.captured())
            
            py_result = py_reg.search(row)
            self.logger.debug('Python re search result: %s' % py_result)
            self.logger.debug('Python re searched[0]: %s' % (py_result[0] if py_result else 'None'))
            
            if py_result:
                display_text = '<span style="color:red;">{}</span>'.format(py_result[0]).join(row.split(py_result[0]))
                self.text_output.append(display_text)
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