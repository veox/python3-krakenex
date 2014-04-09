#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See examples/LICENSE.

# Demonstrates how to use the conditional close functionality; that is,
# placing an order that, once filled, will place another order.
#
# This can be useful for very simple automation, where a bot is not
# needed to constantly monitor execution.

import krakenex

k = krakenex.API()
k.load_key('kraken.key')

k.query_private('AddOrder', {'pair': 'XXBTZEUR',
                             'type': 'buy',
                             'ordertype': 'limit',
                             'price': '1',
                             'volume': '1',
                             'close[pair]': 'XXBTZEUR',
                             'close[type]': 'sell',
                             'close[ordertype]': 'limit',
                             'close[price]': '9001',
                             'close[volume]': '1'})
