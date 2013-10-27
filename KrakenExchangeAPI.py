# Copyright (c) 2013, Noel Maersk <veox tat wemakethings dotnet>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that
# the above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA
# OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import json
import urllib
import urllib2

import hashlib
import hmac
import base64

import time


class KrakenExchangeAPI(object):
    '''Kraken.com cryptocurrency Exchange API'''


    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.version = '0'


    def query_public(self, method, req={}):
        postdata = urllib.urlencode(req)

        headers = {
            'User-Agent': 'Kraken Python API Agent'
        }

        url = self.uri + '/' + self.version + '/public/' + method
        ret = urllib2.urlopen(urllib2.Request(url, postdata, headers))
        return json.loads(ret.read())

        
    def query_private(self, method, req={}):
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
