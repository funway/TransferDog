#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/07 00:13:42

from datetime import datetime

from peewee import Model
from peewee import IntegerField, CharField, DateTimeField


class Processed(Model):
    # 源文件
    source = CharField(null=False)
    
    # 源文件的 mtime
    # 注意 mtime 无固定格式，不同源服务器返回的文件 mtime 可能有所不同。
    mtime = CharField(null=False)
    
    # 处理时间(以文件发送完成时间为记)
    processed_at = DateTimeField(default=lambda: datetime.now())
    
    # 处理进程的 pid
    pid = IntegerField(null=False)
    
    # 任务 id，预留字段，以备后续如果改成多个任务共用一个 processed 文件。
    task_id = CharField(null=True)

    def __str__(self):
        return '{{ id: {id}, source: "{source}", mtime: "{mtime}", processed_at: {processed_at}, pid: {pid}, task_id: {task_id} }}'.format(
            id=self.id, source=self.source, mtime=self.mtime, processed_at=self.processed_at, pid=self.pid, task_id=self.task_id)