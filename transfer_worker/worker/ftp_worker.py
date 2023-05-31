#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/14 09:47:11

import logging, re, threading
from urllib import parse
from ftplib import FTP
from pathlib import Path
from io import BytesIO
from datetime import datetime

from transfer_worker.model.task import Task
from transfer_worker.model.processed import Processed
from transfer_worker.worker.base import Getter, Putter
from transfer_worker.worker.middle_file import MiddleFile
from transfer_worker.utility.ftps import MyFTP_TLS
from transfer_worker.utility.constants import *


class TransferTracker(object):
    def __init__(self, file_size):
        super(TransferTracker, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.WARNING)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        # 文件总大小
        self.total_size = file_size

        # 已传输数据的大小
        self.transfered_size = 0
        return

    def __del__(self):
        self.logger.debug('Delete a %s instance', self.__class__.__name__)
        return

    def transfer_track(self, chunk):
        self.transfered_size += len(chunk)
        self.logger.debug('  Transfer progress: %.2f%% [%s/%sbytes]', 100.0*self.get_progress(),
                          self.transfered_size, self.total_size)
        return

    def is_completed(self):
        result = False
        if self.transfered_size == self.total_size:
            result = True
        return result

    def get_progress(self) -> float:
        """返回传输进度

        Returns:
            float: 0.xx的浮点数
        """
        # 分子分母都加0.001是为了防止分母(文件大小)为0的情况
        return (1.0*self.transfered_size+0.001)/(self.total_size+0.001)
    

def open_ftp(url: str, username: str = None, password: str = None):
    """打开 ftp/ftps 连接

    Args:
        url (str): 以 url 形式表示的 ftp 连接参数。如 ftp://127.0.0.1:21/?encoding=utf8&passive=true 
        username (str, optional): 用户名. Defaults to None.
        password (str, optional): 密码. Defaults to None.

    Raises:
        Exception: _description_

    Returns:
        (FTP, MyFTP_TLS): 返回已建立连接的 ftp/ftps 对象
    """
    o = parse.urlparse(url)
    querys = dict(parse.parse_qsl(o.query))

    if o.scheme == 'ftp':
        ftp = FTP(encoding=querys.get('encoding', 'UTF8'), timeout=FTP_CONNECT_TIMEOUT)
    elif o.scheme == 'ftps':
        ftp = MyFTP_TLS(encoding=querys.get('encoding', 'UTF8'), timeout=FTP_CONNECT_TIMEOUT)
    else:
        raise Exception('Unsupported Protocol: %s' % o.scheme)

    ftp.set_debuglevel(FTP_DEBUG_LEVEL)
    ftp.set_pasv(querys.get('passive', True))

    ftp.connect(o.hostname, 21 if o.port is None else o.port)
    ftp.login(username, password)

    if isinstance(ftp, MyFTP_TLS):
        ftp.prot_p()
    
    return ftp


class FtpGetter(Getter):
    """docstring for FtpGetter."""
    def __init__(self, task: Task):
        super(FtpGetter, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.task = task

        # 源目录
        self.src_path = Path(parse.urlparse(task.source_url).path)

        # 正则表达式
        self.file_pattern = re.compile(self.task.filter_filename)

        self.logger.debug('打开连接: %s', self.task.source_url)
        self.ftp = open_ftp(self.task.source_url, self.task.source_username, self.task.source_password)

        pass

    def __del__(self):
        self.ftp.close()
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
            # MDTM 会以 YYYYmmddHHMMSS(.ms) 的形式返回文件的修改时间，并且是 UTC 的。
            ret = self.ftp.voidcmd('MDTM %s' % f)
            mtime = ret.split()[1]
            self.logger.debug('  文件修改时间: %s', mtime)
            dt_mtime = datetime.strptime(mtime, '%Y%m%d%H%M%S' if len(mtime.split('.')) == 1 else '%Y%m%d%H%M%S.%f')
            if self.task.filter_valid_time > 0 and (datetime.utcnow() - dt_mtime).seconds > self.task.filter_valid_time:
                self.logger.debug('  文件修改时间已超过 %s 秒, 忽略', self.task.filter_valid_time)
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
            path (Path): 开始遍历的根目录(应该使用绝对路径)
            sub (int, optional): 子目录递归层数. Defaults to 0. 负数表示不限制目录深度递归.

        Yields:
            Iterator[Path]: 文件的 Path 对象(全路径)
        """
        self.logger.debug('跳转到目录: %s', path)
        self.ftp.cwd(str(path))

        self.logger.debug('开始遍历目录: %s, recursive sub=%s', path, sub)
        for f in self.ftp.nlst():
            f_is_dir = False
            try:
                # 使用 SIZE 命令来测试 f 是文件还是目录。如果是目录，则 ftp.size() 会抛出异常
                self.ftp.size(str(path.joinpath(f)))
            except Exception as e:
                f_is_dir = True
            
            self.logger.debug('%s %s', 'd' if f_is_dir else 'f', path.joinpath(f))

            if not f_is_dir:
                yield path.joinpath(f)
            elif sub != 0:
                yield from self._iter_path(path.joinpath(f), sub-1)
            
        return 
    
    def get(self, mid_file: MiddleFile, mid_path: Path):
        """下载源文件(mid_file.source)，生成中间临时文件(mid_file.middle)

        如果源文件为大文件，则下载到 mid_path 目录下，将中间文件的全路径赋值给 mid_file.middle
        如果源文件为小文件，则文件内容直接放在 BytesIO 对象中，将该对象赋值给 mid_file.middle
        
        3. remote >> local:  mid_file 就放 dest.path 目录, mid_path = dest.path
        4. remote >> remote: mid_file 就放系统的临时目录, mid_path = tempfile.gettempdir()
        Args:
            mid_file (MiddleFile): _description_
            mid_path (Path): _description_
        """
        assert mid_path is not None, '从远端服务器下载时，中间文件的目录不能为空'

        src_file = str(self.src_path.joinpath(mid_file.source))
        local_tmp_file = mid_path.joinpath(mid_file.source.name + self.task.suffix)

        file_size = self.ftp.size(src_file)
        self.logger.debug('源文件大小: %s bytes', file_size)

        tracker = TransferTracker(file_size)

        def __background():
            self.logger.debug('开始下载文件...')
            try:
                if file_size > MIDDLE_FILE_THRESHOLD:
                    self.logger.debug('大源文件临时保存在本地文件中: %s', local_tmp_file)
                    fp = open(local_tmp_file, 'wb')
                    mid_file.middle = local_tmp_file
                else:
                    self.logger.debug('小源文件临时保存在内存中')
                    fp = BytesIO()
                    mid_file.middle = fp
                
                self.ftp.retrbinary('RETR %s' % src_file,
                               lambda chunk: (fp.write(chunk), tracker.transfer_track(chunk)))
            except Exception as e:
                self.logger.exception('  文件传输时发生异常:')
                exit(-1)
            finally:
                # BytesIO 不需要在这里关闭(如果关闭的话，后续就不再可用了)
                if not isinstance(fp, BytesIO):
                    fp.close()
            return

        t = threading.Thread(target=__background, daemon=True)
        t.start()
        transfered_size = 0
        while t.is_alive():
            # 阻塞主线程，直到超时或线程t结束
            t.join(FTP_TRANSFER_THREAD_JOIN_INTERVAL)

            self.ftp.voidcmd('NOOP')

            # 打印传输进度
            self.logger.debug('  传输进度: %.2f%%', tracker.get_progress() * 100)

            # 判断主线程阻塞期间文件传输是否卡死，如卡死，则跳出循环继续执行主线程。
            if (transfered_size == tracker.transfered_size) and (tracker.transfered_size != 0):
                self.logger.warn('  文件[%s]传输卡死. 进度: %.2f%%', src_file, 100 * tracker.get_progress())
                # 由于python没有提供终止线程的接口，所以只能弃子线程于不顾，继续执行主线程，
                # 主线程运行完后会自动kill所有子线程
                break
            else:
                # 如果没有卡死，赋值last_transfered_size，继续循环等待数据传输子线程
                transfered_size = tracker.transfered_size
            pass

        if not tracker.is_completed():
            self.logger.error('文件传输异常！[%s]', src_file)
            raise Exception("Transfer was not completed")

        return

    def delete_source(self, mid_file: MiddleFile):
        """删除 mid_file 对应的源文件, 删除失败也不抛出异常

        Args:
            mid_file (MiddleFile): _description_
        """
        f = self.src_path.joinpath(mid_file.source)
        self.logger.debug('删除源文件: %s', f)
        try:
            self.ftp.delete(f)
        except Exception as e:
            self.logger.exception('无法删除源文件: %s', f)
        pass


class FtpPutter(Putter):
    def __init__(self, task: Task):
        super(FtpPutter, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        self.task = task

        self.base_path = Path(parse.urlparse(task.dest_url).path)

        self.logger.debug('打开连接: %s', self.task.dest_url)
        self.ftp = open_ftp(self.task.dest_url, self.task.dest_username, self.task.dest_password)
        
        pass

    def __del__(self):
        self.ftp.close()
        pass

    def put(self, mid_file: MiddleFile):
        self.logger.debug('准备上传文件: %s', mid_file)

        dest_file = str(self.base_path.joinpath(mid_file.dest))
        tmp_file = dest_file + (self.task.suffix if self.task.suffix is not None else '')

        self.logger.debug('目标文件: %s', dest_file)
        self.logger.debug('临时文件: %s', tmp_file)
        
        # 获取文件大小
        if isinstance(mid_file.middle, Path):
            file_size = mid_file.middle.stat().st_size
        elif isinstance(mid_file.middle, BytesIO):
            file_size = mid_file.middle.getbuffer().nbytes
        else:
            raise Exception('无法识别的 MiddleFile')
        self.logger.debug('文件大小: %s', file_size)

        # 确保目标文件的远端目录存在
        for d in mid_file.dest.parents[::-1]:
            try:
                p = self.base_path.joinpath(d)
                self.ftp.cwd(str(p))
                self.logger.debug('测试目录 [%s] 是否存在... 通过', p)
            except Exception as e:
                self.logger.warning('目录 [%s] 未找到，新建该目录', p)
                self.ftp.mkd(str(p))

        tracker = TransferTracker(file_size)

        def __background():
            self.logger.debug('开始上传文件...')
            try:
                if isinstance(mid_file.middle, Path):
                    fp = open(mid_file.middle, 'rb')
                else:
                    fp = mid_file.middle
                    fp.seek(0)
                self.ftp.storbinary('STOR %s' % tmp_file, fp, callback=tracker.transfer_track)
            except Exception as e:
                self.logger.exception('  文件传输时发生异常:')
                exit(-1)
            finally:
                fp.close()
            return

        t = threading.Thread(target=__background, daemon=True)
        t.start()
        transfered_size = 0
        while t.is_alive():
            # 阻塞主线程，直到超时或线程 t 结束
            t.join(FTP_TRANSFER_THREAD_JOIN_INTERVAL)
            
            # ftp 有两个通道：数据通道与命令通道。
            # 如果数据通道传输时间太久，而命令通道一直闲置着的话，可能会被防火墙强制关闭命令通道的连接。
            # 发送空命令，尽可能保证命令通道不被关闭（不知道有没效果）
            self.ftp.voidcmd('NOOP')

            # 打印传输进度
            self.logger.debug('  传输进度: %.2f%%', tracker.get_progress() * 100)

            # 判断主线程阻塞期间文件传输是否卡死。如卡死，则跳出循环继续执行主线程。
            if (transfered_size == tracker.transfered_size) and (tracker.transfered_size != 0):
                self.logger.warn('  文件 [%s] 传输卡死. 进度: %.2f%%', dest_file, tracker.get_progress() * 100)
                # 由于 python 没有提供终止线程的接口，所以只能弃子线程于不顾，继续执行主线程，
                # 主线程运行完后会自动 kill 所有子线程
                break
            else:
                # 如果没有卡死，赋值 transfered_size，继续循环等待数据传输子线程
                transfered_size = tracker.transfered_size
            pass

        if not tracker.is_completed():
            self.logger.error('文件传输异常！[%s]', dest_file)
            raise Exception("Transfer was not completed")

        # 修改临时文件名
        if tmp_file != dest_file:
            self.logger.debug('修改临时文件名: %s >> %s', tmp_file, dest_file)
            try:
                self.ftp.delete(dest_file)
            except Exception:
                pass
            finally:
                self.ftp.rename(tmp_file, dest_file)

        pass
