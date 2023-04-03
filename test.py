#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/03/30 21:00:35

'''
单元测试的入口也要放在项目根目录下
'''

import pytest

if __name__ == "__main__":
    # 运行 pytests 目录下的测试用例，并打印详细结果 
    pytest.main(['pytests', '-v']) 