#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/16 10:29:58

import argparse, logging, logging.config, sys

from peewee import SqliteDatabase

from transfer_dog.transfer_worker import TransferWorker
from transfer_dog.model.task import Task
from transfer_dog.utility import constants


def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    parser.add_argument('-i', '--uuid',
                        dest='task_uuid',
                        required=True,
                        help='Task\'s uuid')
    
    parser.add_argument('-d', '--database',
                        dest='db',
                        default=str(constants.CONFIG_DB),
                        help='Task config database. Default is {}'.format(str(constants.CONFIG_DB)))
    
    parser.add_argument('-t', '--table',
                        dest='task_table',
                        default='task',
                        help='Task table in config db. Default is `table`')
    
    parser.add_argument('--log_config',
                        dest='log_config',
                        help='Log config file. Default is None. If you set log_config, then log_file, log_level, log_format will be ignored')
    
    parser.add_argument('--log_file',
                        dest='log_file',
                        help='Log file to output. Default is None')
        
    parser.add_argument('--log_level',
                        dest='log_level',
                        default='WARNING',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Default is WARNING')
    
    parser.add_argument('--log_format',
                        dest='log_format',
                        default='VERBOSE',
                        choices=['SIMPLE', 'VERBOSE'],
                        help='Default is VERBOSE')
    
    args = parser.parse_args()
    return args

LOG_LEVEL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

LOG_FORMAT = {
    'SIMPLE': '%(asctime)s %(levelname)5s - %(message)s',
    'VERBOSE': '%(asctime)s %(levelname)5s [p%(process)d][t%(thread)d] %(name)s.%(funcName)s - %(message)s'
}

if __name__ == "__main__":
    args = parse_arguments()

    if args.log_config is not None:
        try:
            logging.config.fileConfig(args.log_config, encoding='UTF8', defaults={'task_uuid': args.task_uuid} )
        except Exception as e:
            logging.exception('Load logging config file failed! [%s]', args.log_config)
            exit(-1)
    
    # This function does nothing if the root logger already has handlers configured.
    logging.basicConfig(filename=args.log_file, level=LOG_LEVEL[args.log_level], format=LOG_FORMAT[args.log_format])
    
    # 连接数据库
    db = SqliteDatabase(args.db, autoconnect=False)
    db.connect()
    # 绑定模型与表
    models = [Task, ]
    db.bind(models)

    # 创建并启动作业
    worker = TransferWorker(args.task_uuid)
    sys.exit(worker.run())