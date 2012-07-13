# -*- coding: utf-8 -*-
# $File: api.py
# $Date: Fri Jul 13 11:43:37 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""API for accounts9"""

import urllib2
import urllib
import json

from ftp9.config import config
from ftp9.exc import FTP9Error

class Acnt9API(object):
    """accounts9 API class
    
    Raise ftp9.exc.FTP9Error on error"""

    _access_token = None

    def __init__(self, username, passwd):
         data = self._fetch_data('access_token',
                 client_id = config.CLIENT_ID,
                 client_secret = config.CLIENT_SECRET,
                 username = username,
                 password = passwd)
         self._access_token = _get(data, 'access_token')


    def get_user_info(self):
        """Return a dict containing the user information.
        
        Fields: website, bio, givenname, surname, name, mobile, birthdate,
        regtime, groups, address, fullname, password, nickname, email, uid
        """

        return _get(self._fetch_data('userinfo',
            access_token = self._access_token), 'user')

    def get_group_info(self):
        """Return a dict containing the group information."""

        return _get(self._fetch_data('groups',
            access_token = self._access_token,
            interface_secret = config.INTERFACE_SECRET), 'groups')

    def get_group_timestamp(self):
        return unicode(_get(self._fetch_data('grouptimestamp',
            access_token = self._access_token,
            interface_secret = config.INTERFACE_SECRET), 'group_timestamp'))


    def _fetch_data(self, page, **args):
        try:
            try:
                data = urllib2.urlopen(
                    config.ACCOUNTS9_SERVER_ADDR + 'api/' + page + '?' +
                    urllib.urlencode(args)).read()
            except urllib2.HTTPError as e:
                if e.code == 400:
                    raise FTP9Error('incorrect username/password')
                raise
        except urllib2.URLError as e:
            raise FTP9Error('failed to connect to server: {0}'
                    .format(e))

        try:
            data = json.loads(data)
        except ValueError:
            raise FTP9Error('malformed data from server')

        err = data.get('err', None)
        if err:
            raise FTP9Error('error while retrieving information: {0}'.
                    format(err))
        return data



def _get(data, key):
    if key not in data:
         raise FTP9Error('malformed data from server')
    return data[key]

