"""
pytest 如何找到要执行的测试用例

1. 根据命令行参数
  pytest tests/
  pytest tests/test_sample.py
  pytest tests/test_sample.py::test_func

  如果没有指定命令行参数，则查找 pytest.ini 文件中的 testpaths 参数指定

  再没有，则在当前工作目录下查找

2. 会递归子目录

3. 在这些目录下，查找 test_*.py 和 *_test.py 文件

4. 在这些文件中，查找如下两种代码：
  以 test 开头的函数（不在类内部）
  以 Test 开头的类名下的，以 test 开头的类方法
"""
import pytest

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
    with pytest.raises(ZeroDivisionError):
        fun2()