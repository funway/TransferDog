#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  funway.wang
# Created: 2023/05/07 22:24:07


import ftplib, ssl


class MyFTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session

    Python 自带的 ftplib.FTP_TLS 有些 BUG。
    其一是无法重用 TLS 链接。使用此派生类可以避免该问题.
    其二是 storbinary 到 Microsoft IIS ftps 的时候, 会出现链接关闭超时.
    
    参考: https://stackoverflow.com/a/53456626/5777080
        https://bugs.python.org/issue31727
        https://stackoverflow.com/a/50129806/5777080
    """
    def connect(self, host='', port=0, timeout=-999, source_address=None):
        self._no_unwrap_after_stor = False
        
        ret = super().connect(host, port, timeout, source_address)
        
        if 'microsoft' in ret.lower() or 'windows' in ret.lower():
            self._no_unwrap_after_stor = True
        return ret

    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn,
                                            server_hostname=self.host,
                                            session=self.sock.session)  # reuses TLS session            
        return conn, size

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        self.voidcmd('TYPE I')
        with self.transfercmd(cmd, rest) as conn:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)
            # shutdown ssl layer
            if isinstance(conn, ssl.SSLSocket) and not self._no_unwrap_after_stor:
                conn.unwrap()
        return self.voidresp()


if __name__ == "__main__":
    ftps = MyFTP_TLS(encoding='UTF8', timeout=3)
    ftps.set_debuglevel(0)
    ftps.set_pasv(True)

    ftps.connect('win11.vm', 21)
    # ftps.connect('win11.vm', 2121)
    ftps.login('user', 'password')

    ftps.prot_p()
    ftps.retrlines('LIST')