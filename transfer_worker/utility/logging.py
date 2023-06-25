#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/06/25 19:38:43

import logging.handlers
from pathlib import Path

class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    """docstring for ClassName."""

    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False, errors=None):
        
        p = Path(filename).parent
        p.mkdir(parents=True, exist_ok=True)

        super().__init__(filename=filename, mode=mode, maxBytes=maxBytes, 
                         backupCount=backupCount, encoding=encoding, delay=delay, errors=errors)
        pass
    