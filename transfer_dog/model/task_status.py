#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/22 21:26:54

from datetime import datetime

import psutil
from croniter import croniter

class TaskStatus(object):
    """表示任务运行状态的类型

    Args:
        object (_type_): _description_
    """
    def __init__(self, schedule:str, enabled:bool, process:psutil.Process=None):
        super(TaskStatus, self).__init__()
        self.schedule = schedule
        self.enabled = enabled

        self.next_time = croniter(schedule, datetime.now()).get_next(datetime) if enabled else None
        self.last_time = None

        self.process = process
        
        self.need_update = True
        pass

    def __str__(self):
        s = '[p: {p}, last: {last}, next: {next}, schedule: {sche}], {repr}'.format(
            p = None if self.process is None else self.process.pid,
            last = self.last_time,
            next = self.next_time,
            sche = self.schedule,
            repr = object.__repr__(self)
        )
        return s