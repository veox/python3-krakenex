#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Pretty-print a pair's order book depth.

from requests.exceptions import HTTPError

import krakenex

import pprint

kraken = krakenex.API()

try:
    response = kraken.query_public('Depth', {'pair': 'XXBTZUSD', 'count': '10'})
    pprint.pprint(response)
except HTTPError as e:
    print(str(e))
