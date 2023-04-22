#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/01/13 22:22:45

import uuid
from datetime import datetime

from peewee import Model
from peewee import CharField, BooleanField, IntegerField, DateTimeField
from playhouse.shortcuts import model_to_dict, dict_to_model


class Task(Model):
    """docstring for Task."""
    uuid = CharField(unique=True, default=lambda: uuid.uuid4().hex)
    task_name = CharField(default=lambda: datetime.now().strftime('task_%Y%m%d%H%M%S'))
    group_name = CharField(default='Default')
    
    # 任务计划
    schedule = CharField(default='*/5 * * * *')

    # 是否启用
    enabled = BooleanField(default=False)

    # 超时时间，以秒为单位
    timeout = IntegerField(default=60*60)

    # 源地址/目标地址
    # 采用 URL 的格式
    #   协议支持：local, http, ftp, sftp, ftps
    #   将 encoding, passive, keyfile 这些跟服务器相关的参数放在 URL 查询子串中
    source_url = CharField(default='local://127.0.0.1/Users/funway/Downloads/src/?encoding=UTF8')
    dest_url = CharField(default='ftp://funway:caac@172.16.191.128/temp/?encoding=UTF8&passive=True')

    # 文件名过滤规则
    filter_filename = CharField(default='.*')

    # 有效时间过滤规则（只处理 mtime 间隔在此时间内的）
    filter_valid_time = IntegerField(default=-1)

    # 递归多少层子目录，默认为0，不递归子目录
    subdir_recursion = IntegerField(default=0)

    # 是否删除源文件
    delete_source = BooleanField(default=False)

    # 创建时间
    created_at = DateTimeField(default=datetime.now())
    
    # 更新时间
    updated_at = DateTimeField()

    def __str__(self):
        """返回任务实例的 uuid 与实例地址

        Returns:
            string: uuid + object
        """
        return '[%s], %s' % (self.uuid, object.__repr__(self))

    def save(self, force_insert=False, only=None):
        """重写 save()。每次保存之前，先更新 updated_at 字段。然后再调用父类方法。

        Args:
            force_insert (bool, optional): _description_. Defaults to False.
            only (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        self.updated_at = datetime.now()
        return super(Task, self).save(force_insert, only)
    
    def copy(self):
        """Return a copy of the model instance, with [id]=None, [uuid]=new_value, [task_name]=task_name_copy, [enabled]=False, [created_at]=now

        Returns:
            _type_: _description_
        """
        dic = model_to_dict(self)
        
        dic.pop('id')
        dic['uuid'] = uuid.uuid4().hex
        dic['task_name'] = self.task_name + '_copy'
        dic['enabled'] = False
        dic['created_at'] = datetime.now()
        dic['updated_at'] = datetime.now()
        return dict_to_model(Task, dic)