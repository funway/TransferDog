#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/07/15 17:43:36


import logging, time

from transfer_worker.worker.middle_file import Abort, MiddleFile


def process(mid_file: MiddleFile, arg: str) -> None:
    """TransferWorker 在下载完源文件，生成 mid_file.middle 之后，准备上传该 mid_file 之前，会尝试调用中间件的 process() 函数。
    
    此时的 mid_file 只有 {source, source_mtime, middle, abort 属性}

    你可以在 process() 中设置 mid_file 的 dest 与 abort 属性。甚至修改 mid_file.middle 临时文件的内容。

    Args:
        mid_file (MiddleFile): _description_
        arg (str): _description_
    """
    logger = logging.getLogger(__name__)
    logger.debug('rename file: %s', mid_file.source.name)

    name = mid_file.source.name
    new_name = ''
    rules = arg.split(',')
    for rule in rules:

        # 大于 1 的整数，表示取源文件名的第 N 位
        if rule.isdigit():
            if 0 < int(rule) <= len(name):
                new_name += name[int(rule) - 1]
            else:
                logger.warning('无法从源文件名中获取第 %s 位', rule)
        
        # 符号 / 开头的字符串， 表示直接插入该字符串
        elif rule[0] == '/':
            new_name += rule[1:]
        
        # 符号 %s 开头的字符串，表示取时间
        elif rule[0] == '%':
            new_name += time.strftime(rule)

    if new_name == '':
        logger.warning('new_name = source_name, 请检查 rename 规则')
        new_name = mid_file.source.name
    else:
        logger.info('reanme %s to new name: %s', name, new_name)
        mid_file.dest = mid_file.source.parent.joinpath(new_name)
    
    pass