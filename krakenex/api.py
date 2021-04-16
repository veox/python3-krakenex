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

import requests

# private query nonce
import time

# private query signing
import urllib.parse
import hashlib
import hmac
import base64

from . import version

class API(object):
    """ Maintains a single session between this machine and Kraken.

    Specifying a key/secret pair is optional. If not specified, private
    queries will not be possible.

    The :py:attr:`session` attribute is a :py:class:`requests.Session`
    object. Customise networking options by manipulating it.

    Query responses, as received by :py:mod:`requests`, are retained
    as attribute :py:attr:`response` of this object. It is overwritten
    on each query.

    .. note::
       No query rate limiting is performed.

    """
    def __init__(self, key='', secret=''):
        """ Create an object with authentication information.

        :param key: (optional) key identifier for queries to the API
        :type key: str
        :param secret: (optional) actual private key used to sign messages
        :type secret: str
        :returns: None

        """
        self._retry_config = {
            'codes': (504, 520),
            'count': 3,
            'backoff': 1.0,
        }

        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'krakenex/' + version.__version__ + ' (+' + version.__url__ + ')'
        })
        self.response = None
        self._json_options = {}
        return

    def json_options(self, **kwargs):
        """ Set keyword arguments to be passed to JSON deserialization.

        :param kwargs: passed to :py:meth:`requests.Response.json`
        :returns: this instance for chaining

        """
        self._json_options = kwargs
        return self

    def close(self):
        """ Close this session.

        :returns: None

        """
        self.session.close()
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

    @property
    def retry_config(self):
        """ Returns the current retry configuration as a copy.

        :returns: dictionary containing the current retry configuration

        """
        return self._retry_config.copy()

    @retry_config.setter
    def retry_config(self, newconfig):
        """ Sets the retry configuration.

        .. note::
          Checks that keys match in the new and old configurations.

        :param newconfig: new configuration for retries
        :type newconfig: dict

        :returns: None
        :raises: :py:exc:`ValueError` on key count/name mismatch in configurations

        """
        if len(newconfig.keys()) != len(self._retry_config.keys()):
            raise ValueError("Number of keys in current and new configurations does not match!")
        if not all(key in newconfig for key in self._retry_config):
            raise ValueError("New configuration lacks key(s) present in current configuration!")
        if not all(key in self._retry_config for key in newconfig):
            raise ValueError("New configuration specifies extra keys!")

        self._retry_config = newconfig.copy()
        return

    def _retry_session(self, session=None):
        """ Low-level configuration for retries.

        :param session: (optional) An existing session to be used. If ``None``,
                        the session created during instantiation will be used.
        :type session: :py:class:`requests.Session` object

        :returns: :py:class:`requests.Session` object with configured retry adapter

        """
        if session is None:
            session = self.session

        # https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
        retry = requests.packages.urllib3.util.retry.Retry(
            total=pow(self._retry_config['count'], 2),
            connect=self._retry_config['count'],
            read=self._retry_config['count'],
            redirect=0,
            status=self._retry_config['count'],
            method_whitelist=False, # default list doesn't include POST, so force on any verb
            status_forcelist=self._retry_config['codes'],
            backoff_factor=self._retry_config['backoff'],
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)

        session.mount('https://', adapter)
        session.mount('http://', adapter)

        return session

    def _query(self, urlpath, data, headers=None, timeout=None, retry=False):
        """ Low-level query handling.

        .. note::
           Use :py:meth:`query_private` or :py:meth:`query_public`
           unless you have a good reason not to.

        :param urlpath: API URL path sans host
        :type urlpath: str
        :param data: API request parameters
        :type data: dict
        :param headers: (optional) HTTPS headers
        :type headers: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object
        :raises: :py:exc:`requests.HTTPError`: if response status not successful

        """
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        url = self.uri + urlpath

        if retry:
            session = self._retry_session()
        else:
            session = self.session

        self.response = session.post(url, data=data, headers=headers, timeout=timeout)

        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()

        return self.response.json(**self._json_options)


    def query_public(self, method, data=None, timeout=None, retry=False):
        """ Performs an API query that does not require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param data: (optional) API request parameters
        :type data: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object

        """
        if data is None:
            data = {}

        urlpath = '/' + self.apiversion + '/public/' + method

        return self._query(urlpath, data, timeout=timeout, retry=retry)

    def query_private(self, method, data=None, timeout=None, retry=False):
        """ Performs an API query that requires a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param data: (optional) API request parameters
        :type data: dict
        :param timeout: (optional) if not ``None``, a :py:exc:`requests.HTTPError`
                        will be thrown after ``timeout`` seconds if a response
                        has not been received
        :type timeout: int or float
        :returns: :py:meth:`requests.Response.json`-deserialised Python object

        """
        if data is None:
            data = {}

        if not self.key or not self.secret:
            raise Exception('Either key or secret is not set! (Use `load_key()`.')

        data['nonce'] = self._nonce()

        urlpath = '/' + self.apiversion + '/private/' + method

        headers = {
            'API-Key': self.key,
            'API-Sign': self._sign(data, urlpath)
        }

        return self._query(urlpath, data, headers, timeout=timeout, retry=retry)

    def _nonce(self):
        """ Nonce counter.

        :returns: an always-increasing unsigned integer (up to 64 bits wide)

        """
        return int(1000*time.time())

    def _sign(self, data, urlpath):
        """ Sign request data according to Kraken's scheme.

        :param data: API request parameters
        :type data: dict
        :param urlpath: API URL path sans host
        :type urlpath: str
        :returns: signature digest
        """
        postdata = urllib.parse.urlencode(data)

        # Unicode-objects must be encoded before hashing
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        return sigdigest.decode()
