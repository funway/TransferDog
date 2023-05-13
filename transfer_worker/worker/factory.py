#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/09 22:38:27

from urllib import parse
import logging

from transfer_worker.model.task import Task
from transfer_worker.worker.local_woker import LocalGetter, LocalPutter


class GetterFactory(object):
    @classmethod
    def make_getter(clz, task: Task):
        logger = logging.getLogger(clz.__name__)

        o = parse.urlparse(task.source_url)
        logger.debug('src url: %s', task.source_url)
        logger.debug('src url parse result: %s', o)

        if o.scheme == 'local':
            return LocalGetter(task)
        else:
            raise Exception('Unrecognized Source URL')
        pass


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