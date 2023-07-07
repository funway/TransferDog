#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/06/23 12:50:38

import logging, platform, shutil, subprocess
from urllib import parse
from pathlib import Path


def rebuild_standard_url(origin_url: str, username: str = None, password: str = None) -> str:
    """把 username 与 passwor 参数添加到 origin_url 中，构造一个合格的 URL 字符串
    ( 如果 origin_url 的模式是 local:// 的话，替换成标准的 file:// )

    Args:
        origin_url (str): _description_
        username (str): _description_
        password (str): _description_

    Returns:
        str: _description_
    """
    logger = logging.getLogger('helper')
    
    o = parse.urlparse(origin_url)

    if o.scheme == 'local':
        url = 'file://' + o.path 
    else:
        userinfo = None if username is None else username
        userinfo = userinfo if password is None else '{}:{}'.format(userinfo, password)
        netloc = o.netloc if userinfo is None else '{}@{}'.format(userinfo, o.netloc)
        new_o = parse.ParseResult(
            scheme = o.scheme,
            netloc = netloc,
            path = o.path,
            query = '',
            params = '',
            fragment = ''
        )
        url = parse.urlunparse(new_o)
    
    logger.debug('reconstructed standard url: %s', url)
    return url


def show_in_file_manager(url: str, is_file = False):
    """在系统默认的文件管理器(file manager)中打开 url。

    如果 url 是一个本地目录，打开该目录
    如果 url 是一个文件，打开文件所在目录并选中文件（如果允许选中的话）
    如果 url 是一个 ftp 目录，打开该目录

    Args:
        url (str): file://path_to_folder/[filename] or ftp://host/path/
    """
    logger = logging.getLogger('helper')
    logger.info('url: %s', url)

    o = parse.urlparse(url)
    logger.info('url parse: %s', o)
    assert o.scheme in ['file', 'ftp'], 'Unsupported scheme [%s://]' % o.scheme
    
    (cmd, select) = get_file_manager()
    logger.info('get file manager: %s [%s]', cmd, select)
    
    args = [cmd, url]
    
    if is_file and select is not None:
        args.insert(1, select)

    ret = subprocess.run(args)
    logger.info('file manager result: %s', ret)
    return ret.returncode

def get_file_manager():
    """返回一个元组，第一个元素为当前系统的文件管理器命令，第二个元素为该命令下选中文件的参数（如果不支持选中的话为 None）

    Raises:
        Exception: 对于未知的文件管理器则返回异常

    Returns:
        _type_: (fm_cmd, select_arg)
    """
    system = platform.system()

    if system == 'Windows':
        return ('explorer.exe', '/select,')
    elif system == 'Darwin':
        return ('open', '-R')
    elif system == 'Linux':
        if shutil.which('nautilus'):
            return ('nautilus', '--select')
        elif shutil.which('dolphin'):
            return ('dolphin', '--select')
        elif shutil.which('thunar'):
            return ('thunar', None)
        elif shutil.which('nemo'):
            return ('nemo', None)
        elif shutil.which('peony'):
            return ('peony', '--show-items')
        elif shutil.which('dde-file-manager'):
            return ('dde-file-manager', '--show-item')
        else:
            pass

    raise Exception('Unknown file manager')