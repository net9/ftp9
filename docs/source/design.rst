..  $File: design.rst
    $Date: Sun Aug 12 17:40:11 2012 +0800
    $Author: jiakai<jia.kai66@gmail.com>


Design Overview
---------------

A modified version of `pyftpdlib <http://code.google.com/p/pyftpdlib/>`_ 0.7.0
is used as the FTP back-end.

:class:`Authorizer <ftp9.auth.Authorizer>` is the authentication and
authorization class, whose interface is defined by pyftpdlib. When a new
connection is established, :class:`Acnt9API <ftp9.api.Acnt9API>` is invoked to
authenticate the user name and password using `Accounts9 API
<https://wiki.net9.org/w/Net9Auth>`_, and then
:meth:`Group.update <ftp9.group.Group.update>` is called to synchronize group
information. :meth:`Authorizer.has_perm <ftp9.auth.Authorizer.has_perm>` is used
for permission check, but underlying `authorization strategy
<https://wiki.net9.org/w/Ftp9>`_ is implemented in ``src/ftp9/group.py``.

``src/ftp9/config.py`` is the configuration file template, but it is tracked by git.
So custom configuration should be written in ``src/ftp9/config_overwrite.py``, in
which a function with signature ``def overwrite_config(conf)`` should be
defined to modify the :class:`Config <ftp9.config.Config>` instance passed to it.

*Note:*
    #. pyftpdlib is an asynchronous FTP server library, and currently only one
       worker process is used. If support for multiple workers is desired, a
       filesystem lock should be used in :meth:`Group.update
       <ftp9.group.Group.update>`.
    #. Currently the IPv6 address of Accounts9 server is not accessible, but
       ``accounts.net9.org`` has an AAAA record, so the python2 socket library
       is hacked to avoid timing out on trying to connect to the IPv6 address.
       See ``src/ftp9/__init__.py`` for details.


| Jiakai <jia.kai66[at]gmail.com>
| Aug. 12, 2012
