# -*- coding: utf-8 -*-
# $File: auth.py
# $Date: Tue Jul 03 11:48:37 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""provides an authorizer integrated with Accouts9 for pyftpdlib"""

from pyftpdlib import ftpserver

import os

class Authorizer(ftpserver.DummyAuthorizer):
    def validate_authentication(self, username, passwd):
        print "auth", username, passwd
        return True

    def get_home_dir(self, username):
        print "hw", username
        return os.getcwd()

    def get_msg_login(self, username):
        return "welcome, " + username + "!"

    def get_msg_quit(self, username):
        return "goodbye!"

    def get_perms(self, username):
        ftpserver.logerror("unsuppoted operation: Authorizer.get_perms")
        return ""

    def has_perm(self, username, perm, path = None):
        print "has perm", username, perm, path
        return True


def get_authorizer():
    return Authorizer()

