..  $File: index.rst
    $Date: Sun Aug 12 11:59:48 2012 +0800
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

    #. Create ``src/config_overwrite.py`` to set custom configuration.

       Example:

           .. code-block:: python

               def overwrite_config(conf):
                   conf.FTP_BIND = ('', 21)
                   conf.FTP_ROOT = '/data/ftp'

    
    #. Execute ``start.sh`` to start the server.

Contents:

.. toctree::
    :maxdepth: 2

    api



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

