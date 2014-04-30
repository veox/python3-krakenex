# This file is part of krakenex.
#
# krakenex is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# krakenex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General
# Public LICENSE along with krakenex. If not, see
# <http://www.gnu.org/licenses/gpl-3.0.txt>.


import json
import urllib.request, urllib.parse, urllib.error

# private query nonce
import time

# private query signing
import hashlib
import hmac
import base64

from krakenex import connection


class API:
    """Kraken.com cryptocurrency Exchange API.
    
    Public methods:
    load_key
    query_public
    query_private
    
    """
    def __init__(self, key = '', secret = '', conn = None):
        """Create an object with authentication information.
        
        Arguments:
        key    -- key required to make queries to the API (default: '')
        secret -- private key used to sign API messages (default: '')
        conn   -- krakenex.Connection object for connection reuse
                  (default: None)
        
        """
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.conn = conn


    def load_key(self, path):
        """Load key and secret from file.
        
        Argument:
        path -- path to file (string, no default)
        
        """
        f = open(path, "r")
        self.key = f.readline().strip()
        self.secret = f.readline().strip()


    def set_connection(self, conn):
        """Set an existing connection to be used as a default in queries.

        Argument:
        conn -- connection (krakenex.Connection object, no default)

        """
        self.conn = conn


    def _query(self, urlpath, req = {}, conn = None, headers = {}):
        """Low-level query handling.
        
        Arguments:
        urlpath -- API URL path sans host (string, no default)
        req     -- additional API request parameters (default: {})
        conn    -- kraken.Connection object (default: None)
        headers -- HTTPS headers (default: {})
        
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
        """API queries that do not require a valid key/secret pair.
        
        Arguments:
        method -- API method name (string, no default)
        req    -- additional API request parameters (default: {})
        conn   -- connection object to reuse (default: None)
        
        """
        urlpath = '/' + self.apiversion + '/public/' + method

        return self._query(urlpath, req, conn)

    
    def query_private(self, method, req={}, conn = None):
        """API queries that require a valid key/secret pair.
        
        Arguments:
        method -- API method name (string, no default)
        req    -- additional API request parameters (default: {})
        conn   -- connection object to reuse (default: None)
        
        """
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
