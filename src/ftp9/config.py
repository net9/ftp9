# -*- coding: utf-8 -*-
# $File: config.py
# $Date: Sun Aug 12 12:07:37 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""server configuration, see the source for details"""

class _Config:
    FTP_BIND = ('', 8021)

    FTP_ROOT = '/tmp/ftp9'

    FTP_DISCARDED_GROUP = '/tmp/ftp9-old'
    # when group structure gets changed, directories for groups that no longer
    # exist will be moved to this directory; set to None to remove those
    # directories directly

    FTP_MAX_CONS = 0
    FTP_MAX_CONS_PER_IP = 0
    # maximum simultaneous FTP connections; 0 for unlimited


    ACCOUNTS9_SERVER_ADDR = 'https://accounts.net9.org/'

    FILESYSTEM_ENCODING = 'utf-8'
    USERNAME_ENCODING = 'utf-8'

    CLIENT_ID = 'RYDzVZQ5FuQc9-bfyb2xQb8HeiU'
    CLIENT_SECRET = '8nyXuWB7dqNcshu5ZQ1B'
    INTERFACE_SECRET = 'dYpo6zB1m7azVpL'

config = _Config()

from config_overwrite import overwrite_config as _oc
_oc(config)
