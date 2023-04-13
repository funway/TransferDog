#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/01/13 22:22:45

import uuid
from datetime import datetime

from peewee import Model
from peewee import CharField, BooleanField, IntegerField, DateTimeField


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

    created_at = DateTimeField(default=datetime.now())
    update_at = DateTimeField()

    def __str__(self):
        """返回任务实例的 uuid 与实例地址

        Returns:
            string: uuid + object
        """
        return '[%s], %s' % (self.uuid, object.__repr__(self))

    def save(self, force_insert=False, only=None):
        """重写 save()。每次保存之前，先更新 update_at 字段。然后再调用父类方法。

        Args:
            force_insert (bool, optional): _description_. Defaults to False.
            only (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        self.update_at = datetime.now()
        return super(Task, self).save(force_insert, only)