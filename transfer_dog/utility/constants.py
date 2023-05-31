#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2022/12/26 15:15:50

# from os import path
from pathlib import Path

APP_NAME = 'TransferDog'
APP_VERSION = '0.0.2'

# 包目录
PACKAGE_PATH = Path(__file__).parent.parent

# 项目目录
PROJECT_PATH = PACKAGE_PATH.parent

# 中间件目录
MIDDLEWARE_PATH = PROJECT_PATH / 'plugin/middleware/'

# 项目配置文件
APP_CONFIG = PROJECT_PATH / 'conf/app.conf'

# 日志配置文件
LOGGING_CONFIG = PROJECT_PATH / 'conf/app_logging.conf'

# 任务数据库
TASK_DB = PROJECT_PATH / 'conf/task.db'

# 静态资源目录
RESOURCE_PATH = PACKAGE_PATH / 'resource'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

_IP_FIELD = '(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])'
REGEX_IP_ADDRESS = '^' + _IP_FIELD + '\.' + _IP_FIELD + '\.' + _IP_FIELD + '\.' + _IP_FIELD + '$'
