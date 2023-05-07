#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/07 22:24:07

import ftplib, ssl

class ReusedSSLSocket(ssl.SSLSocket):
    def unwrap(self):
        pass


class MyFTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session

    Python 自带的 ftplib.FTP_TLS 有个 BUG, 无法重用 TLS 链接。使用此派生类可以避免该问题.
    
    参考: https://stackoverflow.com/a/53456626/5777080
        https://bugs.python.org/issue31727
    """
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn,
                                            server_hostname=self.host,
                                            session=self.sock.session)  # reuses TLS session            
            conn.__class__ = ReusedSSLSocket  # we should not close reused ssl socket when file transfers finish
        return conn, size
    

if __name__ == "__main__":
    ftps = MyFTP_TLS()
    ftps.set_debuglevel(2)
    ftps.connect('win11.vm', 21)
    ftps.login('user', 'password')
    ftps.prot_p()
    ftps.retrlines('LIST')
    