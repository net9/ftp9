# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Oct 06 22:58:42 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

def _force_ipv4():
    import socket
    orig = socket.getaddrinfo

    def getaddrinfo(host, port, family = 0, socktype = 0, proto = 0, flags = 0):
        if family == socket.AF_UNSPEC:
            family = socket.AF_INET
        return orig(host, port, family, socktype, proto, flags)
    socket.getaddrinfo = getaddrinfo

from ftp9.config import config

def _patch_path_join():
    import os.path
    orig = os.path.join
    def join(*args):
        args = list(args)
        for i in range(len(args)):
            if type(args[i]) is unicode:
                args[i] = args[i].encode(config.FILESYSTEM_ENCODING)
        return orig(*args)
    os.path.join = join


_force_ipv4()
_patch_path_join()

from pyftpdlib import ftpserver

from ftp9.handler import FTPHandler

import pwd

class Server(ftpserver.FTPServer):
    max_cons = config.FTP_MAX_CONS
    max_cons_per_ip = config.FTP_MAX_CONS_PER_IP


def run_server():
    """call this function to start the ftp server"""
    uid = None
    gid = None
    if config.DAEMON_USER:
        t = pwd.getpwnam(config.DAEMON_USER)
        (uid, gid) = (t.pw_uid, t.pw_gid)
    Server(config.FTP_BIND, FTPHandler, uid, gid).serve_forever()

