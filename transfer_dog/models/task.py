#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/01/13 22:22:45

import uuid
from datetime import datetime

from peewee import Model
from peewee import CharField, BooleanField, IntegerField


class Task(Model):
    """docstring for Task."""
        
    uuid = CharField(unique=True, default=lambda: uuid.uuid4().hex)
    task_name = CharField(default=lambda: datetime.now().strftime('task_%Y%m%d%H%M%S'))
    group_name = CharField(default='Default')
    schedule = CharField(default='*/5 * * * *')
    enabled = BooleanField(default=False)

    source_server = CharField(default='local://')
    source_encoding = CharField(default='UTF8')
    source_passive_mode = BooleanField(default=True)
    source_path = CharField(default='')

    filter_filename = CharField(default='.*')
    filter_valid_time = IntegerField(default=-1)
    scan_subdir = BooleanField(default=False)
    delete_source = BooleanField(default=False)

    dest_server = CharField(default='local://')
    dest_encoding = CharField(default='UTF8')
    dest_passive_mode = BooleanField(default=True)
    dest_path = CharField(default='')
