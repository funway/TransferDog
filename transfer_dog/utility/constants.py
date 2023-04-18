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

# 项目配置文件
APP_CONFIG = PROJECT_PATH / 'conf/app.conf'

# 日志配置文件
LOGGING_CONFIG = PROJECT_PATH / 'conf/app_logging.conf'

# 任务数据库
TASK_DB = PROJECT_PATH / 'conf/task.db'

# 静态资源目录
RESOURCE_PATH = PACKAGE_PATH / 'resource'