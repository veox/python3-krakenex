# This file is part of krakenex.
#
# krakenex is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# krakenex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser
# General Public LICENSE along with krakenex. If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> and
# <http://www.gnu.org/licenses/gpl-3.0.txt>.

"""Kraken.com cryptocurrency Exchange API."""

import urllib.request
import urllib.parse
import urllib.error

# private query nonce
import time

# private query signing
import hashlib
import hmac
import base64

from . import connection

class API(object):
    """ Maps a key/secret pair to a connection.

    Specifying either the pair or the connection is optional.

    .. note::
       If a connection is not set, a new one will be opened on
       first query. If a connection is set, during creation or as a result
       of a previous query, it will be reused for subsequent queries.
       However, its state is not checked.

    .. note::
       No timeout handling or query rate limiting is performed.

    .. note::
       If a private query is performed without setting a key/secret
       pair, the effects are undefined.

    """
    def __init__(self, key='', secret='', conn=None):
        """ Create an object with authentication information.

        :param key: key required to make queries to the API
        :type key: str
        :param secret: private key used to sign API messages
        :type secret: str
        :param conn: existing connection object to use
        :type conn: krakenex.Connection
        :returns: None

        """
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.conn = conn
        return

    def load_key(self, path):
        """ Load key and secret from file.

        Expected file format is key and secret on separate lines.

        :param path: path to keyfile
        :type path: str
        :returns: None

        """
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()
        return

    def _query(self, urlpath, data, conn=None, headers=None):
        """ Low-level query handling.

        If a connection object is provided, attempts to use that
        specific connection.

        If it is not provided, attempts to reuse a connection from the
        previous query.

        If this is the first ever query, opens a new connection, and
        keeps it as a fallback for future queries.

        Connection state is not checked.

        .. warning::
           The fallback connection will be re-used for both public and
           private queries.

        .. note::
           Preferably use :py:meth:`query_private` or
           :py:meth:`query_public` instead.

        :param urlpath: API URL path sans host
        :type urlpath: str
        :param req: API request parameters
        :type req: dict
        :param conn: (optional) existing connection object to use
        :type conn: krakenex.Connection
        :param headers: (optional) HTTPS headers
        :type headers: dict
        :returns: :py:func:`json.loads`-deserialised Python object

        """
        url = self.uri + urlpath

        if conn is None:
            if self.conn is None:
                self.conn = connection.Connection()
            conn = self.conn

        if headers is None:
            headers = {}

        return conn._request(url, data, headers)

    def query_public(self, method, data=None, conn=None):
        """ API queries that do not require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object

        """
        urlpath = '/' + self.apiversion + '/public/' + method

        if data is None:
            data = {}

        return self._query(urlpath, data, conn)

    def query_private(self, method, data=None, conn=None):
        """ API queries that require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object

        """
        if data is None:
            data = {}

        # TODO: allow using a different scheme
        data['nonce'] = int(1000*time.time())

        # TODO: check if self.{key,secret} are set
        urlpath = '/' + self.apiversion + '/private/' + method

        headers = {
            'API-Key': self.key,
            'API-Sign': self._sign(data, urlpath)
        }

        return self._query(urlpath, data, conn, headers)

    def _sign(self, data, urlpath):
        """ TODO

        TODO
        """
        postdata = urllib.parse.urlencode(data)

        # Unicode-objects must be encoded before hashing
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        return sigdigest.decode()
