#!/bin/bash
# $File: start.sh
# $Date: Fri Jul 13 11:10:27 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. ./init.sh
cd src
$PYTHON -c 'import ftp9; ftp9.run_server()'

