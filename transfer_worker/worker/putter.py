#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/05 21:38:06

from abc import ABCMeta, abstractmethod
from datetime import datetime
from urllib import parse
from pathlib import Path
import logging, re, shutil

from transfer_worker.model.task import Task
from transfer_worker.worker.middle_file import MiddleFile

class PutterFactory(object):
    @classmethod
    def make_putter(clz, task: Task):
        logger = logging.getLogger(clz.__name__)

        o = parse.urlparse(task.dest_url)
        logger.debug('dest url: %s', task.dest_url)
        logger.debug('dest url parse result: %s', o)

        if o.scheme == 'local':
            return LocalPutter(task)
        else:
            raise Exception('Unrecognized Dest URL')
        pass

class Putter(metaclass=ABCMeta):
    @abstractmethod
    def put(self):
        pass

class LocalPutter(Putter):
    def __init__(self, task: Task):
        super(LocalPutter, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.task = task
        
        self.dest = parse.urlparse(task.dest_url)
        querys = dict(parse.parse_qsl(self.dest.query))

        # 目标目录
        self.dest_path = Path(self.dest.path)
        assert self.dest_path.is_dir(), '[{path}] is not a valid directory'.format(path=self.dest_path)
        
        # 临时文件后缀，缺省为 .tmp
        self.temp_suffix = querys.get('suffix', '.tmp') 
        
        pass
    
    def put(self, mid_file: MiddleFile):
        self.logger.debug('开始上传文件: %s', mid_file)

        dest_path = self.dest_path.joinpath(mid_file.dest).parent
        if not dest_path.exists():
            self.logger.debug('创建目标目录: %s', dest_path)
            dest_path.mkdir(parents=True)
        
        shutil.move(mid_file.middle, self.dest_path.joinpath(mid_file.dest))
        pass