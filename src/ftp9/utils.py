# -*- coding: utf-8 -*-
# $File: utils.py
# $Date: Sat Sep 22 09:20:01 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""miscellaneous helper functions"""

import os
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
    return os.path.relpath(fs_enc(path), config.FTP_ROOT)

def fs_enc(val, path = None):
    """if val is not Unicode, convert it to Unicode using
    config.FILESYSTEM_ENCODING
    if failed to decode and `path` is not None, then try other encodings and
    rename the file if successful (`path` should be the base directory)"""
    if isinstance(val, str):
        try:
            val = val.decode(config.FILESYSTEM_ENCODING)
        except UnicodeDecodeError:
            pass
    return val

