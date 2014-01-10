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

import httplib
import urllib


class Connection:
    """Kraken.com connection handler.

    Public methods:
    close
    """


    def __init__(self, uri = 'api.kraken.com', timeout = 30):
        """ Create an object for reusable connections.
        
        Arguments:
        uri     -- URI to connect to (default: 'https://api.kraken.com')
        timeout -- blocking operations' timeout in seconds (default: 30)
        """
        self.headers = {
            'User-Agent': 'krakenex/0.0.3 (+https://github.com/veox/krakenex)'
        }

        self.conn = httplib.HTTPSConnection(uri, timeout = timeout)


    def close(self):
        """ Close the connection.

        No arguments.
        """
        self.conn.close()


    def _request(self, url, req = {}, headers = {}):
        """ Send POST request to API server.
        
        url     -- Fully-qualified URL with all necessary urlencoded
                   information (string, no default)
        req     -- additional API request parameters (default: {})
        headers -- additional HTTPS headers, such as API-Key and API-Sign
                   (default: {})
        """
        data = urllib.urlencode(req)
        headers.update(self.headers)

        self.conn.request("POST", url, data, headers)
        response = self.conn.getresponse()

        return response.read()
