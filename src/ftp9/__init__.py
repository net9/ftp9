# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Tue Jul 03 10:41:10 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ftp9 import handler
from ftp9 import conf
from pyftpdlib import ftpserver

def run_server():
    """call this function to start the ftp server"""

    ftpserver.FTPServer(conf.ADDRESS, handler.get_ftp_handler()).serve_forever()

