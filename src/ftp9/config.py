# -*- coding: utf-8 -*-
# $File: config.py
# $Date: Sun Aug 12 17:18:10 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""Server configuration file template. Note that custom configuration should be
defined in ``src/ftp9/config_overwrite.py``. """

class Config(object):
    FTP_BIND = ('', 8021)

    FTP_ROOT = '/tmp/ftp9'

    FTP_DISCARDEDGRP_SAVEDIR = '/tmp/ftp9-old'
    """When group structure gets changed, directories for groups that no longer
    exist will be moved to this directory; set to None to remove those
    directories directly."""

    FTP_MAX_CONS = 0
    """maximum simultaneous FTP connections; 0 for unlimited"""

    FTP_MAX_CONS_PER_IP = 0
    """maximum simultaneous FTP connections per IP address; 0 for unlimited"""


    ACCOUNTS9_SERVER_ADDR = 'https://accounts.net9.org/'

    FILESYSTEM_ENCODING = 'utf-8'
    USERNAME_ENCODING = 'utf-8'

    CLIENT_ID = ''
    CLIENT_SECRET = ''
    INTERFACE_SECRET = ''

    ROOTGRP_NAME = 'authorized'
    """name of the group corresponding to FTP_ROOT in the filesystem"""

    PUBLIC_NAME = u'public'
    """name of the public directory for each group"""

    PRIVATE_NAME = u'private'
    """name of the private directory for each group"""

config = Config()

from config_overwrite import overwrite_config as _oc
_oc(config)
