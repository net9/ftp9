#!/bin/bash
# $File: ftp9_server.sh
# $Date: Tue Jul 03 09:45:20 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

PYTHON=python2

export PYTHONDONTWRITEBYTECODE=1
$PYTHON -c 'import ftp9; ftp9.run_server()'

