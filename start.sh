#!/bin/bash
# $File: start.sh
# $Date: Wed Aug 15 09:07:37 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. ./init.sh
cd src
exec $PYTHON -c 'import ftp9; ftp9.run_server()'

