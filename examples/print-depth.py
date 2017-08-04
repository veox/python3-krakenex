#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Pretty-print a pair's order book depth.

import krakenex

import pprint

k = krakenex.API()

response = k.query_public('Depth', {'pair': 'XXBTZUSD', 'count': '10'})
pprint.pprint(response)
