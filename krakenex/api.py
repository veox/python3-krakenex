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
# <http://www.gnu.org/licenses/lgpl-3.0.txt>.


"""Kraken.com cryptocurrency Exchange API."""


import json
import urllib.request, urllib.parse, urllib.error

# private query nonce
import time

# private query signing
import hashlib
import hmac
import base64

from . import connection


class API(object):
    """ Maps a key/secret pair to a connection.

    Specifying either is optional.

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
    def __init__(self, key = '', secret = '', conn = None):
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


    # FIXME: use @property instead?
    def set_connection(self, conn):
        """ Set an existing connection to be used as a default in queries.

        .. note:: May become deprecated in future versions.

        :param conn: existing connection object to use
        :type conn: krakenex.Connection
        :returns: None

        """
        self.conn = conn
        return


    def _query(self, urlpath, req = {}, conn = None, headers = {}):
        """ Low-level query handling.

        Preferrably use :py:meth:`query_private` or
        :py:meth:`query_public` instead.

        :param urlpath: API URL path sans host
        :type urlpath: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: existing connection object to use
        :type conn: krakenex.Connection
        :param headers: HTTPS headers
        :type headers: dict
        :returns: :py:func:`json.loads`-deserialised Python object
        
        """
        url = self.uri + urlpath

        if conn is None:
            if self.conn is None:
                conn = connection.Connection()
            else:
                conn = self.conn

        ret = conn._request(url, req, headers)
        return json.loads(ret)

    
    def query_public(self, method, req = {}, conn = None):
        """ API queries that do not require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: existing connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        
        """
        urlpath = '/' + self.apiversion + '/public/' + method

        return self._query(urlpath, req, conn)

    
    def query_private(self, method, req={}, conn = None):
        """ API queries that require a valid key/secret pair.
        
        :param method: API method name
        :type method: str
        :param req: additional API request parameters
        :type req: dict
        :param conn: existing connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        
        """
        # TODO: check if self.{key,secret} are set
        urlpath = '/' + self.apiversion + '/private/' + method

        req['nonce'] = int(1000*time.time())
        postdata = urllib.parse.urlencode(req)

        # Unicode-objects must be encoded before hashing
        encoded = (str(req['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        headers = {
            'API-Key': self.key,
            'API-Sign': sigdigest.decode()
        }

        return self._query(urlpath, req, conn, headers)
