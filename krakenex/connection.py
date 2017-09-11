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

"""Connection handling."""

import http.client
import urllib.request
import urllib.parse
import urllib.error

from . import version


class Connection(object):
    """ Object representing a single connection.

    Opens a reusable HTTPS connection. Allows specifying HTTPS timeout,
    or server URI (for testing purposes).

    """

    def __init__(self, uri='api.kraken.com', timeout=30):
        """ Create an object for reusable connections.

        :param uri: URI to connect to
        :type uri: str
        :param timeout: blocking operations' timeout (in seconds)
        :type timeout: int
        :returns: None

        """
        self.headers = {
            'User-Agent': 'krakenex/' + version.__version__ +
            ' (+' + version.__url__ + ')'
        }
        self.conn = http.client.HTTPSConnection(uri, timeout=timeout)
        return

    def close(self):
        """ Close this connection.

        :returns: None

        """
        self.conn.close()
        return

    def _request(self, url, req=None, headers=None):
        """ Send POST request to API server using this connection.

        If not provided, sets empty request parameters and HTTPS
        headers for this request.

        :param url: fully-qualified URL with all necessary urlencoded
             information
        :type url: str
        :param req: (optional) API request parameters
        :type req: dict
        :param headers: (optional) HTTPS headers, such as API-Key and API-Sign
        :type headers: dict
        :returns: :py:mod:`http.client`-decoded response
        :raises: :py:exc:`http.client.HTTPException`: if response status not
             successful

        """

        if req is None:
            req = {}

        if headers is None:
            headers = {}

        data = urllib.parse.urlencode(req)
        headers.update(self.headers)

        self.conn.request('POST', url, data, headers)
        response = self.conn.getresponse()

        if response.status not in (200, 201, 202):
            raise http.client.HTTPException(response.status)

        return response.read().decode()
