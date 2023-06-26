#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/04/16 10:29:58

import argparse, logging, logging.config, sys, threading, time
from pathlib import Path

import psutil

from transfer_worker.transfer_worker import TransferWorker
from transfer_worker.model.task import Task


def suicide_when_parent_exited():
    """新建子线程，在子线程中定时轮询父进程是否已经死亡。如果父进程已死，则杀死自身进程。
    """
    
    def _polling_in_sub_thread(parent_proc):
        logging.debug('Start a sub thread, polling to check parent process [p%s]', parent_proc.pid)

        # 每 {polling_gap} 秒轮询一次，检查父进程是否已死
        polling_gap = 0.5
        while parent_proc.is_running():  
            time.sleep(polling_gap)

        logging.warning('Parent process dead. Commit suicide.')
        psutil.Process().kill()
        pass

    self_proc = psutil.Process()
    try:
        parent_proc = psutil.Process(pid=self_proc.ppid())
    except Exception as e:
        logging.exception('Can not get parent process. Commit suicide.')
        self_proc.kill()
    
    if parent_proc.pid == 1:
        logging.warning('Parent process dead (ppid=1). Commit suicide.')
        self_proc.kill()

    t = threading.Thread(target=_polling_in_sub_thread, kwargs={'parent_proc': parent_proc}, daemon=True)
    t.start()
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    parser.add_argument('-i', '--uuid',
                        metavar='UUID',
                        dest='task_uuid',
                        required=True,
                        help='Task\'s uuid')
    
    parser.add_argument('-d', '--database',
                        dest='db',
                        required=True,
                        help='Task config database')
    
    parser.add_argument('-p', '--processed',
                        dest='processed',
                        help='Processed history. Default is \'working_path/processed/uuid.db\'')
    
    parser.add_argument('--daemon',
                        dest='daemon',
                        action=argparse.BooleanOptionalAction,
                        help='Run as daemon process, exited when parent process dead. Default is --no-daemon')
    
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

def main():
    args = parse_arguments()
    print('Command Line Args:', args)

    # 设置 logging
    if args.log_config is not None:
        try:
            logging.config.fileConfig(args.log_config, encoding='UTF8', defaults={'task_uuid': args.task_uuid} )
        except Exception as e:
            logging.exception('Load logging config file failed! [%s]', args.log_config)
            exit(2)
    # This function does nothing if the root logger already has handlers configured.
    logging.basicConfig(filename=args.log_file, level=LOG_LEVEL[args.log_level], format=LOG_FORMAT[args.log_format])

    if args.processed is None:
        processed = Path(__file__).parent.joinpath('processed', args.task_uuid + '.db')
        processed.parent.mkdir(parents=True, exist_ok=True)
        args.processed = str(processed)

    # 启动子线程轮询父进程是否退出
    if args.daemon:
        suicide_when_parent_exited()
        pass
    
    try:
        # 创建并启动作业
        worker = TransferWorker(task_uuid=args.task_uuid, task_db=args.db, processed_db=args.processed)
        ret = worker.run()
    except Exception as e:
        logging.exception('Unexpected running error!')
        ret = 1
    finally:
        sys.exit(ret)

if __name__ == "__main__":
    main()