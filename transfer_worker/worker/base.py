#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/09 22:40:56

from abc import ABCMeta, abstractmethod
from pathlib import Path

from transfer_worker.worker.middle_file import MiddleFile


class Getter(metaclass=ABCMeta):
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def get(self, mid_file: MiddleFile, mid_path: Path):
        pass
    
    @abstractmethod
    def delete_source(self, mid_file: MiddleFile):
        pass


class Putter(metaclass=ABCMeta):
    @abstractmethod
    def put(self):
        pass