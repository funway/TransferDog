#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/16 10:09:37

import logging

from transfer_dog.model.task import Task

class TransferWorker(object):
    """docstring for TransferWorker."""
    def __init__(self, task_uuid: str):
        super(TransferWorker, self).__init__()
        # 设置 logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)
        
        self.task = self.load_task(task_uuid)

        pass

    def load_task(self, task_uuid):
        try:
            assert Task.table_exists(), 'Task 表不存在！'
        except Exception as e:
            self.logger.error('Task 表不存在！')
            raise e

        self.logger.debug('Load task [%s]', task_uuid)
        task = Task.get_or_none(Task.uuid == task_uuid)

        try:
            assert task is not None, 'Can not find the task!'
        except Exception as e:
            self.logger.error('Can not find the task!')
            raise e
        
        return task

    def run(self) -> int:
        """运行作业

        Returns:
            int: 运行结果。0 表示正常结束，1 表示执行异常
        """
        
        
        self.logger.debug('Working...')
        
        return 0