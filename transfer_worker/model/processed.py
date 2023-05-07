#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/07 00:13:42

from datetime import datetime

from peewee import Model
from peewee import IntegerField, CharField, DateTimeField


class Processed(Model):
    source = CharField(null=False)
    mtime = CharField(null=False)
    processed_at = DateTimeField(default=datetime.now())
    pid = IntegerField(null=False)

    def __str__(self):
        return '{{ id: {id}, source: "{source}", mtime: "{mtime}", processed_at: {processed_at}, pid: {pid} }}'.format(
            id=self.id, source=self.source, mtime=self.mtime, processed_at=self.processed_at, pid=self.pid)