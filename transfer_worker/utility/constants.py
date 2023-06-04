#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/27 09:41:14

FTP_DEBUG_LEVEL = 0

FTP_CONNECT_TIMEOUT = 3

# 传输线程探活的时间间隔(主线程会 JOIN 等待传输线程该秒数，判断传输线程有没卡死)
TRANSFER_THREAD_JOIN_INTERVAL = 10

# 过滤源文件时，忽略文件修改时间 mtime 与当前时间之差在该值以内的文件
IGNORE_MTIME_IN_SECONDS = 1

# middle file 保存为本地临时文件的阈值，小于该值的直接保存在内存中(BytesIO)
MIDDLE_FILE_THRESHOLD = 1024 * 1024




