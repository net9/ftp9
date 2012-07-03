# -*- coding: utf-8 -*-
# $File: handler.py
# $Date: Tue Jul 03 10:45:58 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""generate the ftp handler used for pyftpdlib"""

from ftp9 import auth

from pyftpdlib.ftpserver import FTPHandler

def get_ftp_handler():
    class Handler(FTPHandler):
        authorizer = auth.get_authorizer()

    return Handler

