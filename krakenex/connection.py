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

class KrakenConnection(object):
    """Kraken.com connection handler.

    Public methods:
    close
    """

    def __init__(self, uri = 'https://api.kraken.com', timeout = 30):
        """ Create an object for reusable connections.
        
        Arguments:
        uri     -- URI to connect to (default: 'https://api.kraken.com')
        timeout -- blocking operations timeout in seconds (default: 30)
        """
        self.headers = {
            'User-Agent': 'Kraken Python API Agent'  # TODO: version
        }

        self.conn = httplib.HTTPSConnection(uri, timeout = timeout)

    def close(self):
        """ Close the connection.

        No arguments.
        """
        self.conn.close()

    def _request(self, url, data = {}, headers = {}):
        """ TODO

        headers -- additional user-provided HTTP headers, such as
                   API-Key and API-Sign (default: {})
        """
        headers.update(self.headers)

        self.conn.request("POST", url, data, headers)
        response = self.conn.getresponse()

        return response.read()
