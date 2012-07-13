# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Fri Jul 13 11:15:17 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

def _force_ipv4():
    import socket
    orig = socket.getaddrinfo

    def getaddrinfo(host, port, family = 0, socktype = 0, proto = 0, flags = 0):
        if family == socket.AF_UNSPEC:
            family = socket.AF_INET
        return orig(host, port, family, socktype, proto, flags)
    socket.getaddrinfo = getaddrinfo

_force_ipv4()


from pyftpdlib import ftpserver

from ftp9.auth import Authorizer
from ftp9.config import config
from ftp9.group import Group

class Handler(ftpserver.FTPHandler):
    authorizer = Authorizer(Group())

class Server(ftpserver.FTPServer):
    max_cons = config.FTP_MAX_CONS
    max_cons_per_ip = config.FTP_MAX_CONS_PER_IP

def run_server():
    """call this function to start the ftp server"""
    Server(config.FTP_BIND, Handler).serve_forever()

