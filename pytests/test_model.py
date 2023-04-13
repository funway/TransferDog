from PySide6.QtCore import QRegularExpression

from transfer_dog.model import Task

def test_Task():
    t = Task()
    print('')
    print(t)
    print(t.id)
    print(t.created_at)
    print(t.update_at)

def test_QRegularExpression():
    text = 'xeshi任务'
    reg = 'c*'
    filterRegularExpression = QRegularExpression(reg, options=QRegularExpression.PatternOption.CaseInsensitiveOption)
    print(filterRegularExpression.match(text))
    print(filterRegularExpression.match(text).captured())
    
