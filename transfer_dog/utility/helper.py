#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/06/23 12:50:38

import logging
from urllib import parse


def rebuild_standard_url(origin_url: str, username: str, password: str):
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