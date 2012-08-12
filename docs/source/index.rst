..  $File: index.rst
    $Date: Sun Aug 12 17:16:41 2012 +0800
    $Author: jiakai<jia.kai66@gmail.com>


Welcome to ftp9's documentation!
=================================

Welcome! This documentation is generated on |today| for ftp9 |release|.

ftp9 is a simple FTP server based on pyftpdlib, integrated with Accounts9
authentication system.

Quickstart:

    #. Create ``init.sh`` in the source root so that environment variable
       ``PYTHON`` can be set to point to your python2 interpreter.

       Example:

           .. code-block:: sh

               echo 'export PYTHON=python2' > init.sh

    #. Create ``src/ftp9/config_overwrite.py`` to set custom configuration. See
       ``src/ftp9/config.py`` for available options.

       Example:

           .. code-block:: python

               def overwrite_config(conf):
                   conf.FTP_BIND = ('', 21)
                   conf.FTP_ROOT = '/data/ftp'
                   conf.FTP_DISCARDEDGRP_SAVEDIR = '/data/ftp.old'
                   conf.CLIENT_ID = '<your clien id here>'
                   conf.CLIENT_SECRET = '<your client secret here>'
                   conf.INTERFACE_SECRET = '<the interface secret here>'

    #. Execute ``start.sh`` to start the server.

Contents:

.. toctree::
    :maxdepth: 2

    design
    api



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

