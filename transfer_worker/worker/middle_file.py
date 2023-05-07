#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/04 23:03:13

from enum import Enum
from pathlib import Path


class Abort(Enum):
    ABORT = 1
    """中止操作
    """
    
    ABORT_AND_RECORD = 2
    """中止操作并记录
    """
    
    NO_ABORT = 0
    """不中止操作
    """


class MiddleFile(object):
    def __init__(self, source: Path, source_mtime, middle = None, dest: Path = None, abort: Abort = Abort.NO_ABORT):
        """MiddleFile 做为从 Getter 获取的临时文件，等待 Putter 将其上传到目标地址

        Args:
            source (Path): 源文件（相对于 task.source.path 的相对路径，前面没有 / 符号）

            source_mtime (_type_): 源文件修改时间

            middle (_type_, optional): 中间文件，本地(临时)文件的全路径，或者是一个内存流对象. Defaults to None.

            dest (Path, optional): 目标文件（相对于 task.dest.path 的相对路径，前面没有 / 符号）. Defaults to None.
            
            abort (Abort, optional): 是否中止处理（不再进行 Putter 操作）. Defaults to Abort.NO_ABORT.
        """
        super(MiddleFile, self).__init__()
        
        # 源(相对于 task.source.path 的路径)
        self.source = source
        
        # 源文件的 mtime
        self.source_mtime = source_mtime

        # 中间文件的全路径（或者流对象）
        self.middle = middle
        
        # 目标(相对于 task.dest.path 的路径)
        self.dest = dest
        
        # 是否中止处理
        self.abort = abort
        pass

    def __str__(self) -> str:
        return str(self.__dict__)
    