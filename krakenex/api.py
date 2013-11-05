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
import urllib
import urllib2

import hashlib
import hmac
import base64

import time


class API(object):
    """Kraken.com cryptocurrency Exchange API.
    
    Public methods:
    query_public
    query_private
    
    """
    
    def __init__(self, key = '', secret = ''):
        """Create an object with authentication information.
        
        Arguments:
        key    -- key required to make queries to the API (default '')
        secret -- private key used to sign API messages (default '')
        
        """
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.version = '0'
    
    def query_public(self, method, req = {}):
        """API queries that do not require a valid key/secret pair.
        
        Arguments:
        method -- API method name (string, no default)
        req    -- additional request parameters (default {})
        
        """
        postdata = urllib.urlencode(req)
        
        headers = {
            'User-Agent': 'Kraken Python API Agent'
        }
        
        url = self.uri + '/' + self.version + '/public/' + method
        ret = urllib2.urlopen(urllib2.Request(url, postdata, headers))
        return json.loads(ret.read())
    
    def query_private(self, method, req={}):
        """API queries that require a valid key/secret pair.
        
        Arguments:
        method -- API method name (string, no default)
        req    -- additional request parameters (default {})
        
        """
        req['nonce'] = int(1000*time.time())
        postdata = urllib.urlencode(req)
        
        urlpath = '/' + self.version + '/private/' + method
        message = urlpath + hashlib.sha256(str(req['nonce']) +
                                            postdata).digest()
        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        
        headers = {
            'User-Agent': 'Kraken Python API Agent',
            'API-Key': self.key,
            'API-Sign': base64.b64encode(signature.digest())
        }
        
        url = self.uri + urlpath
        ret = urllib2.urlopen(urllib2.Request(url, postdata, headers))
        return json.loads(ret.read())
