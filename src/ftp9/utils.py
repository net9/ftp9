# -*- coding: utf-8 -*-
# $File: utils.py
# $Date: Sun Aug 12 21:27:50 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""miscellaneous helper functions"""

import os.path

from ftp9.config import config

def human_readable_filesize(size):
    """return a human-readable string representation of the file size specified
    by ``size`` in bytes."""
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    pos = 0
    while size > 1024:
        size /= 1024.0
        pos += 1

    if isinstance(size, float):
        fmt = '{0:.2f}{1}'
    else:
        fmt = '{0}{1}'
    return fmt.format(size, units[pos])


def relpath(path):
    """return a relative path to the FTP root"""
    if isinstance(path, str):
        path = path.decode(config.FILESYSTEM_ENCODING)
    return os.path.relpath(path, config.FTP_ROOT)
