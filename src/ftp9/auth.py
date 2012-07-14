# -*- coding: utf-8 -*-
# $File: auth.py
# $Date: Sat Jul 14 19:29:33 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

import os
import os.path

from pyftpdlib import ftpserver

from ftp9.api import Acnt9API
from ftp9.exc import FTP9Error
from ftp9.config import config

class Authorizer(ftpserver.DummyAuthorizer):
    """authorizer used for pyftpdlib"""

    _group_info = None

    def __init__(self, grp):
        """:param grp: a :class:`ftp9.group.Group` instance used for manipulating group
        information"""
        super(Authorizer, self).__init__()
        self._group_info = grp

    def validate_authentication(self, username, passwd):
        try:
            api = Acnt9API(username, passwd)
        except Exception as e:
            return 'failed to login: {0}'.format(e)
        self._group_info.update(api)
        return True

    def get_home_dir(self, username):
        return config.FTP_ROOT

    def get_msg_login(self, username):
        return "welcome, " + username + "!"

    def get_msg_quit(self, username):
        return "goodbye!"

    def get_perms(self, username):
        ftpserver.logerror("unsupported operation: Authorizer.get_perms")
        return ""

    _perm_map = {'e': 'read', 'l': 'read', 'r': 'read', 'a': 'modify',
            'd': 'modify', 'f': 'modify', 'm': 'write', 'w': 'write',
            'M': 'modify'}
    def has_perm(self, username, perm, path = None):
        path = path.decode(config.FILESYSTEM_ENCODING)
        parts = path.split(u'/')
        for i in range(len(parts)):
            base = parts[i]
            if base == 'public' or base == 'private':
                g = self._group_info.get_node_by_path(u'/'.join(parts[:i]))
                if not g:
                    return False
                return username.decode(config.USERNAME_ENCODING) in getattr(g,
                        base + '_' + self._perm_map[perm])

        return True

