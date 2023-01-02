#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/12/26 15:15:50

from os import path

APP_NAME = 'TransferDog'
APP_VERSION = '0.0.1'

# 程序主目录
BASE_PATH = path.dirname(path.dirname(__file__))

# 程序配置文件
CONFIG_DB = BASE_PATH + '/conf/config.db'

CONFIG_TABLE_TASKS = 'tasks'

LOGGING_CONFIG = BASE_PATH + '/conf/logging.conf'