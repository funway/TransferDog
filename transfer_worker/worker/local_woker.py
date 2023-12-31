#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/09 22:44:03

from datetime import datetime
from urllib import parse
from pathlib import Path
from io import BytesIO
import logging, re, shutil, os

from transfer_worker.model.task import Task
from transfer_worker.model.processed import Processed
from transfer_worker.worker.base import Getter, Putter
from transfer_worker.worker.middle_file import MiddleFile
from transfer_worker.utility.constants import *

    
class LocalGetter(Getter):
    def __init__(self, task: Task):
        super(LocalGetter, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.task = task
        
        # 源目录
        p = parse.urlparse(task.source_url).path
        if os.name == 'nt':
            p = p[1:]
        self.src_path = Path(p)
        assert self.src_path.is_dir(), '[{path}] is not a valid directory'.format(path=self.src_path)

        # 正则表达式
        self.file_pattern = re.compile(self.task.filter_filename)

        pass
    
    def next(self):
        """生成器：遍历 task.source.path 路径，获取待处理文件的 MiddleFile 对象

        Yields:
            MiddleFile: {source, source_mtime}
        """
        for f in self._iter_path(self.src_path, self.task.subdir_recursion):
            # 通过 _iter_path 遍历目录下所有文件
            self.logger.debug('判断文件 %s', f)
            
            # 1. 判断文件修改时间
            mtime = f.stat().st_mtime
            dt_mtime = datetime.fromtimestamp(mtime)
            self.logger.debug('  文件修改时间: %s', dt_mtime)
            
            now = datetime.now()
            if self.task.filter_valid_time > 0 and (now - dt_mtime).seconds > self.task.filter_valid_time:
                self.logger.debug('  文件修改时间(%s)与当前时间(%s)差超过 %s 秒, 忽略', dt_mtime, now, self.task.filter_valid_time)
                continue
            
            if (now - dt_mtime).seconds < IGNORE_MTIME_IN_SECONDS:
                self.logger.debug('  文件修改时间(%s)与当前时间(%s)差小于 %s 秒, 忽略', dt_mtime, now, IGNORE_MTIME_IN_SECONDS)
                continue

            self.logger.debug('  判断文件修改时间... 通过')

            # 2. 判断文件名是否匹配正则表达式
            # 注意 re.search() 与 re.match() 的区别
            match = self.file_pattern.search(str(f))
            # match = self.file_pattern.search(str(f.name))
            if not match:
                self.logger.debug('  文件名不匹配, 忽略')
                continue
            self.logger.debug('  判断文件名匹配... 通过')

            mid_file = MiddleFile(f.relative_to(self.src_path), str(mtime))

            # 3. 判断文件是否已处理
            processed = Processed.get_or_none(source=mid_file.source, mtime=mid_file.source_mtime)
            # processed = Processed.select().where(
            #                         Processed.source==str(mid_file.source), Processed.mtime==str(mid_file.source_mtime)
            #                     ).order_by(Processed.processed_at.desc()).get_or_none()
            if processed is not None:
                self.logger.debug('  文件已处理，忽略. processed = %s', processed)
                continue
            self.logger.debug('  判断是否未处理... 通过')

            # 4. yield 一个中间对象
            yield mid_file

        pass
    
    def _iter_path(self, path: Path, sub = 0) -> Path:
        """生成器：遍历 path 路径，获取所有文件（不包括文件夹）

        Args:
            path (Path): 开始遍历的根目录
            sub (int, optional): 子目录递归层数. Defaults to 0. 负数表示不限制目录深度递归.

        Yields:
            Iterator[Path]: 文件的 Path 对象(全路径)
        """
        assert path.is_dir(), 'path must be a directory'
        self.logger.debug('开始遍历目录: %s, recursive sub=%s', path, sub)
        for f in path.iterdir():
            self.logger.debug('%s %s', 'd' if f.is_dir() else 'f', f)
            if not f.is_dir():
                yield f
            elif sub !=0:
                yield from self._iter_path(f, sub-1)
        pass

    def delete_source(self, mid_file: MiddleFile):
        """删除 mid_file 对应的源文件, 删除失败也不抛出异常

        Args:
            mid_file (MiddleFile): _description_
        """
        f = self.src_path.joinpath(mid_file.source)
        self.logger.debug('删除源文件: %s', f)
        try:
            f.unlink()
        except Exception as e:
            self.logger.exception('无法删除源文件: %s', f)
        pass

    def get(self, mid_file: MiddleFile, mid_path: Path):
        """从源文件获取中间态文件，放到 mid_path 下。
        1. local >> local:  mid_file.middle 就放 dest.path 目录, 所以需要拷贝一份文件到 dest.path
        2. local >> remote: mid_file.middle 就是源文件

        Args:
            mid_file (MiddleFile): _description_
            mid_path (Path): _description_
        """
        if mid_path is None:
            # local >> remote
            # 中间文件就是源文件
            mid_file.middle = self.src_path.joinpath(mid_file.source)
        else:
            # local >> local
            mid_file.middle = mid_path.joinpath(mid_file.source.name + self.task.suffix)
            shutil.copy(self.src_path.joinpath(mid_file.source), mid_file.middle)
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
        self.dest_path = Path(self.dest.path[1:] if os.name=='nt' else self.dest.path)
        assert self.dest_path.is_dir(), '[{path}] is not a valid directory'.format(path=self.dest_path)
        
        pass
    
    def put(self, mid_file: MiddleFile):
        self.logger.debug('开始上传文件: %s', mid_file)

        dest_path = self.dest_path.joinpath(mid_file.dest).parent
        if not dest_path.exists():
            self.logger.debug('创建目标目录: %s', dest_path)
            dest_path.mkdir(parents=True)
        
        if isinstance(mid_file.middle, Path):
            # 如果 mid_file.middle 是一个文件路径
            shutil.move(mid_file.middle, self.dest_path.joinpath(mid_file.dest))
        elif isinstance(mid_file.middle, BytesIO):
            # 如果 mid_file.middle 是一个内存对象
            with open(self.dest_path.joinpath(mid_file.dest), 'wb') as fp:
                fp.write(mid_file.middle.getvalue())
        else:
            raise Exception('无法识别的中间文件类型: %s', mid_file.middle)
        pass