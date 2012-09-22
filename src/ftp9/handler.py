# -*- coding: utf-8 -*-
# $File: handler.py
# $Date: Sat Sep 22 09:25:25 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

import logging
import os.path

from pyftpdlib import ftpserver

from ftp9.auth import Authorizer
from ftp9.config import config
from ftp9.group import Group
from ftp9.utils import human_readable_filesize, relpath, fs_enc

_loggers = [
        logging.getLogger('access'),
        logging.getLogger('modify'),
        logging.getLogger('error')]

for i in range(3):
    hdl = config.LOG_HANDLERS[i]
    if not hdl:
        hdl = logging.StreamHandler()
        hdl.setFormatter(logging.Formatter('[%(asctime)s] %(message)s',
            '%Y-%m-%d %T'))
    lg = _loggers[i]
    lg.setLevel(logging.INFO)
    lg.addHandler(hdl)

_log_access = _loggers[0].info
_log_modify = _loggers[1].info
_log_error = _loggers[2].info

class AbstractedFS(ftpserver.AbstractedFS):
    def listdir(self, path, handler):
        ret = list()
        for i in super(AbstractedFS, self).listdir(path):
            try:
                idec = i.decode(config.FILESYSTEM_ENCODING)
            except UnicodeDecodeError:
                idec = ''
                for enc in config.FILESYSTEM_POSSIBLE_ENCODINGS:
                    try:
                        new = i.decode(enc)
                    except UnicodeDecodeError:
                        continue
                    new_enc = new.encode(config.FILESYSTEM_ENCODING)
                    os.rename(os.path.join(path, i),
                            os.path.join(path, new_enc))
                    i = new_enc
                    idec = new
            if idec not in (config.PUBLIC_NAME, config.PRIVATE_NAME) \
                    or handler.authorizer.has_perm(
                            handler.username, "l", os.path.join(path, i)):
                ret.append(i)
        return ret

    def get_list_dir(self, path, handle):
        if self.isdir(path):
            lst = self.listdir(path, handle)
            lst.sort()
            return self.format_list(path, lst)
        else:
            basedir, filename = os.path.split(path)
            self.lstat(path)  # raise exc in case of problems
            return self.format_list(basedir, [filename])


class FTPHandler(ftpserver.FTPHandler):
    """customized FTP handler"""

    authorizer = Authorizer(Group())
    abstracted_fs = AbstractedFS

    def run_as_current_user(self, func, *args, **kargs):
        if func.func_code is AbstractedFS.listdir.func_code or \
                func.func_code is AbstractedFS.get_list_dir.func_code:
            return func(args[0], self)
        return super(FTPHandler, self).run_as_current_user(func, *args, **kargs)

    def log(self, msg, logger = _log_access):
        """derived method"""
        logger(u"[{self.username}@{self.remote_ip}:{self.remote_port}] {msg}".
                format(self = self, msg = msg))

    def log_error(self, msg):
        self.log(msg, _log_error)

    logline = log

    def log_cmd(self, cmd, arg, respcode, respstr):
        """derived method"""
        if cmd in ("DELE", "RMD", "RNFR", "RNTO", "MKD"):
            arg = relpath(arg)
            if respcode < 400:
                self.log(u'{0} {1}: {2}'.format(cmd, arg, respcode),
                        _log_modify)
            else:
                self.log(u'{0} {1}: {2} {3}'.format(cmd, arg, respcode,
                    respstr.decode(config.FILESYSTEM_ENCODING)), _log_modify)

    def log_transfer(self, cmd, filename, receive, completed, elapsed, bytes):
        """derived method"""
        if elapsed > 0:
            filename = relpath(filename)
            size = human_readable_filesize(bytes)
            speed = human_readable_filesize(bytes / elapsed) + '/s'
            msg = u'{0} {1}: size={2} time={3:.1f}sec speed={4}'.format(
                    cmd, filename, size, elapsed, speed)
            if not completed:
                msg += ' [uncompleted]'
            if receive:
                self.log(msg, _log_modify)
            else:
                self.log(msg, _log_access)


