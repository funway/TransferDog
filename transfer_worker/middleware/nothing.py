#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/05 14:46:48

import logging

from transfer_worker.worker.middle_file import MiddleFile


def pre_process(mid_file: MiddleFile, arg: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug('Just do nothing.')
    pass

def process(mid_file: MiddleFile, arg: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug('Just do nothing.')
    pass