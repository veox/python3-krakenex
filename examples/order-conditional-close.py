#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Demonstrates how to use the conditional close functionality; that is,
# placing an order that, once filled, will place another order.
#
# This can be useful for very simple automation, where a bot is not
# needed to constantly monitor execution.
#
# Complex nesting seems to not be allowed by Kraken. See:
# https://github.com/veox/python3-krakenex/issues/39

import krakenex

def main():
    kraken = krakenex.API()
    kraken.load_key('kraken.key')

    response = kraken.query_private('AddOrder',
                                    {'pair': 'XXBTZEUR',
                                     'type': 'buy',
                                     'ordertype': 'limit',
                                     'price': '1',
                                     'volume': '1',
                                     # `ordertype`, `price`, `price2` are valid
                                     'close[ordertype]': 'limit',
                                     'close[price]': '9001',
                                     # these will be ignored!
                                     'close[pair]': 'XXBTZEUR',
                                     'close[type]': 'sell',
                                     'close[volume]': '1'})
    return response

if __name__ == '__main__':
    ret = main()
    print(ret)
