#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/16 10:09:37

import logging, time

from peewee import OperationalError

from transfer_worker.model.task import Task

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
        self.logger.debug('Load task [%s]', task_uuid)

        try:
            task = Task.get_or_none(Task.uuid == task_uuid)
            assert task is not None, 'Can not find the task!'
        except OperationalError as e:
            self.logger.exception('Task 表异常!')
            raise e
        except Exception as e:
            self.logger.exception('无法找任务[%s]!', task_uuid)
            raise e
        
        return task

    def run(self) -> int:
        """运行作业

        Returns:
            int: 运行结果。0 表示正常结束，1 表示执行异常
        """
        self.logger.info('开始作业 [%s]: %s', self.task.uuid, self.task.task_name)

        count = len(self.task.task_name) * 10
        while count > 0:
            self.logger.debug('Working...')
            count -= 1
            time.sleep(3)
        
        self.logger.info('完成作业 [%s]: %s', self.task.uuid, self.task.task_name)
        return 0
