#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/01 14:59:17

from transfer_dog.utility.constants import *

def test_logging_config():
    assert LOGGING_CONFIG.exists()

def test_config_db():
    assert CONFIG_DB.exists()