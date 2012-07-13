..  $File: index.rst
    $Date: Fri Jul 13 11:09:01 2012 +0800
    $Author: jiakai<jia.kai66@gmail.com>


Welcome to ftp9's documentation!
=================================

Welcome! This documentation is generated on |today| for ftp9 |release|.

ftp9 is a simple FTP server based on pyftpdlib, integrated with Accounts9
authentication system.

Quickstart:

    #. Create ``init.sh`` in the source root so that environment variable
       ``PYTHON`` can be set appropriately to your python2 interpreter.

       Example:

           .. code-block:: sh

               echo 'export PYTHON=python2' > init.sh

    #. Modify src/ftp9/config.py
    
    #. Execute ``start.sh`` to start the server.

Contents:

.. toctree::
    :maxdepth: 2

    api



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

