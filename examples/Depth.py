#!/usr/bin/env python3
# pretty-print the depth on a pair

import pprint
import krakenex

k = krakenex.API()

response = k.query_public('Depth', {'pair': 'XXBTZUSD', 'count': '10'})
pprint.pprint(response)
