# -*- coding: utf-8 -*-
# $File: auth.py
# $Date: Fri Aug 31 22:29:18 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

import os
import os.path
from hashlib import md5

from pyftpdlib import ftpserver

from ftp9.api import Acnt9API
from ftp9.exc import FTP9Error
from ftp9.config import config
from ftp9.utils import fs_enc

class Authorizer(ftpserver.DummyAuthorizer):
    """authorizer used for pyftpdlib"""

    _group_info = None
    _root_path_len = None
    _home = None

    def __init__(self, grp):
        """:param grp: a :class:`ftp9.group.Group` instance used for manipulating group
        information"""
        super(Authorizer, self).__init__()
        self._group_info = grp
        self._root_path_len = len(config.FTP_ROOT.split(u'/'))
        self._home = config.FTP_ROOT
        if isinstance(self._home, unicode):
            self._home = self._home.encode(config.FILESYSTEM_ENCODING)

    def validate_authentication(self, username, passwd):
        if username == config.FTP_ADMIN_USERNAME:
            return md5(passwd).hexdigest() == config.FTP_ADMIN_PASSWD_MD5

        try:
            api = Acnt9API(username, passwd)
        except Exception as e:
            return 'failed to login: {0}'.format(e)
        self._group_info.update(api)
        if username not in self._group_info.authed_users:
            return 'failed to login: unauthorized user'

    def get_home_dir(self, username):
        return self._home

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
        username = fs_enc(username)
        path = fs_enc(path)
        parts = path.split(u'/')
        if len(parts) > self._root_path_len and \
                parts[self._root_path_len] == config.ROOT_PUB_NAME:
            if username == config.FTP_ADMIN_USERNAME:
                return True
            return self._perm_map[perm] != 'modify'

        for i in range(self._root_path_len, len(parts)):
            base = parts[i]
            if base == config.PUBLIC_NAME or base == config.PRIVATE_NAME:
                if username == config.FTP_ADMIN_USERNAME:
                    return True
                base = 'public' if base == config.PUBLIC_NAME else 'private' 
                g = self._group_info.get_node_by_path(u'/'.join(parts[:i]))
                if not g:
                    return False
                return username in getattr(g, base + '_' + self._perm_map[perm])

        return perm in ['e', 'l']

