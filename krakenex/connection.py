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
# <http://www.gnu.org/licenses/gpl-3.0.txt>.


import http.client
import urllib.request, urllib.parse, urllib.error


class Connection(object):
    """Kraken.com connection handler.

    """


    def __init__(self, uri = 'api.kraken.com', timeout = 30):
        """ Create an object for reusable connections.
        
        :param uri: URI to connect to.
        :type uri: str
        :param timeout: blocking operations' timeout (in seconds).
        :type timeout: int
        :returns: TODO
        :raises: TODO
        
        """
        self.headers = {
            'User-Agent': 'krakenex/0.1.0 (+https://github.com/veox/python3-krakenex)'
        }
        self.conn = http.client.HTTPSConnection(uri, timeout = timeout)


    def close(self):
        """ Close the connection.

        """
        self.conn.close()


    def _request(self, url, req = {}, headers = {}):
        """ Send POST request to API server.
        
        :param url: fully-qualified URL with all necessary urlencoded
            information
        :type url: str
        :param req: additional API request parameters
        :type req: dict
        :param headers: additional HTTPS headers, such as API-Key and API-Sign
        :type headers: dict

        """
        data = urllib.parse.urlencode(req)
        headers.update(self.headers)

        self.conn.request("POST", url, data, headers)
        response = self.conn.getresponse()

        return response.read().decode()
