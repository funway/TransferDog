def fun1(x):
    return x + 1

def fun2():
    return 1/0

def test_fun1_equal():
    """测试案例：确认 fun1(3) 返回值等于 4
    """
    import sys
    assert fun1(3) == 4

def test_fun2_error():
    """测试案例：确认 fun2() 函数一定会抛出 ZeroDivisionError 异常
    """
    import pytest
    with pytest.raises(ZeroDivisionError):
        fun2()