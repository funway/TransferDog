#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/06/29 23:59:24

import logging, sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtCore import QSystemSemaphore, QByteArray, QCoreApplication, Qt

class SingleAppGuard(object):
    """docstring for SingleAppGuard.
    QLocalSocket 在 Unix 类系统使用 Unix domain socket 作为底层实现，在 Windows 系统使用命名管道作为底层实现

    由于并不是真实的网络连接，所以 QLocalSocket 并不需要等待 “握手” 完成。
    只要服务端已经开始 listen(), 那么在 QLocalSocket.connectToServer() 之后，这个连接其实就已经建立了。
    客户端可以不需要 waitForConnected() 就直接开始 write() 数据了。
    服务端可以不需要 nextPendingConnection() 来获取该连接, 如果它并不想知道客户端发了什么消息过来，也没打算回消息的话。

    如果不存在 server, 客户端 error() 将返回 ServerNotFoundError 错误
    如果存在一个残留的已崩溃的 server, 客户端 error() 将返回 LocalSocketError.ConnectionRefusedError 错误
    """
    def __init__(self, app_id, raise_error = True):
        super(SingleAppGuard, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Init a %s instance', self.__class__.__name__)

        if QCoreApplication.instance() is None:
            warning = """A QObject instance (like {}.server) created before QCoreApplication (or QGuiApplication/QApplication) initialized, its signal/slot will not be handled by the main event loop!
            """.format(self.__class__.__name__)
            self.logger.warning(warning)

        self.app_id = app_id
        self.server = None

        self._is_another_running = False
        
        # 获取互斥信号量，同时只允许有一个进程进入下面步骤
        _sema = QSystemSemaphore(app_id, 1, mode=QSystemSemaphore.AccessMode.Open)
        _sema.acquire()
        self.logger.debug('已取得系统信号量: %s', _sema)

        _client = QLocalSocket()
        self.logger.debug('创建本地 socket: %s [%s]', _client, _client.state())

        # 尝试连接服务器（第一个启动的程序实例会创建一个 QLocalServer 服务器)
        _client.connectToServer(app_id)
        self._is_another_running = _client.waitForConnected()

        if self._is_another_running:
            self.logger.warning('另一个程序实例已启动')
            
            # _client.write(QByteArray('Hello! From PID[%s]' % os.getpid()))
            # _client.flush()
            
            if raise_error:
                _sema.release()
                raise Exception('另一个程序实例已启动')
        else:
            self.logger.debug('无法建立连接: %s [%s]', _client.error(), _client.state())
            
            self.server = QLocalServer()
            # unix 类系统的在程序崩溃的时候不会自动释放 unix socket
            # 所以这里需要尝试 remove 一下，把上次奔溃残留的 unix socket 删除（如果有的话）
            self.server.removeServer(app_id)

            # 启动监听
            ret = self.server.listen(app_id)
            if ret:
                self.logger.debug('QLocalServer 开始监听: %s', self.server.fullServerName())
            else:
                self.logger.warning('QLocalServer 无法启动监听. %s', self.server.serverError())
                _sema.release()
                raise Exception('QLocalServer 无法启动监听')
        
        # 释放信号量
        _sema.release()
        self.logger.debug('已释放系统信号量')
        pass
    
    def is_another_running(self):
        return self._is_another_running
    
    def is_listening(self):
        return False if self.server is None else self.server.isListening()

    def __del__(self):
        self.logger.debug('Delete a %s instance', self.__class__.__name__)
        pass

def raise_window(window: QMainWindow):
    """将隐藏或者最小化的窗口 “尽可能地” 显示到桌面最前端。不同操作系统下该函数的效果也不一致，甚至可能无效。

    Args:
        window (QMainWindow): _description_
    """
    # 将 invisible 的窗口变成 visible
    window.show()

    # 将最小化的窗口变成活跃窗口(minimized 与 invisible 是两个概念)
    window.setWindowState((window.windowState() & ~Qt.WindowState.WindowMinimized) | Qt.WindowState.WindowActive)
    
    # 将不在桌面 front 的窗口提升到最前端显示(macOS 有效)
    window.raise_()
    
    # 如果窗口不是最前端窗口，
    # Windows 任务栏上的程序图标会闪烁(Windows 不修改注册表的话，好像只能做到这样了)
    # Ubuntu 则会在桌面弹出一个系统提示(Ubuntu 也无法将程序窗口直接提升到桌面最前端)
    window.activateWindow()
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s pid[%(process)d] %(levelname)5s %(name)s.%(funcName)s - %(message)s')

    app = QApplication(sys.argv)
    guard = SingleAppGuard('me.hawu.test')

    window = QMainWindow()
    window.show()

    if guard.is_listening():
        logging.debug('服务器正在监听')
        guard.server.newConnection.connect(lambda: logging.debug('有新连接'))
        guard.server.newConnection.connect(lambda: raise_window(window))

    ret = app.exec()

    sys.exit(ret)
