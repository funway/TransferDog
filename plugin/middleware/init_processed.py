#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/07 15:42:55

import logging

from transfer_worker.worker.middle_file import MiddleFile, Abort

DESCRIPTION = """本中间件可以用来初始化对应任务的 processed 数据库。
将所有文件记录到 processed 数据库中，但并不真正执行下载与传输操作。
"""

def pre_process(mid_file: MiddleFile, arg: str) -> None:
    logger = logging.getLogger(__name__)
    
    mid_file.abort = Abort.ABORT_AND_RECORD
    pass