from PySide6.QtCore import QRegularExpression
from playhouse.shortcuts import model_to_dict, dict_to_model

from transfer_worker.model import Task

def test_Task():
    t = Task()
    print(model_to_dict(t))
    tt = t.replica()
    print(model_to_dict(tt))

def test_QRegularExpression():
    text = 'xeshi任务'
    reg = 'c*'
    filterRegularExpression = QRegularExpression(reg, options=QRegularExpression.PatternOption.CaseInsensitiveOption)
    print(filterRegularExpression.match(text))
    print(filterRegularExpression.match(text).captured())
    
