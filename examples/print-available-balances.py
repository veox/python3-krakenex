#!/usr/bin/env python

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Get balance available for trading/withdrawal (not on orders).
#
# NOTE: Assumes regular orders. Margin positions are not taken into account!
#
# FIXME: Also shows how current krakenex usage has too much sugar.

import krakenex

from decimal import Decimal as D
import pprint

k = krakenex.API()
k.load_key('kraken-monitor.key')

balance = k.query_private('Balance')
orders = k.query_private('OpenOrders')

balance = balance['result']
orders = orders['result']

newbalance = dict()
for currency in balance:
    # remove first symbol ('Z' or 'X'), but not for GNO
    newname = currency[1:] if len(currency) == 4 else currency
    newbalance[newname] = D(balance[currency]) # type(balance[currency]) == str
balance = newbalance

for _, o in orders['open'].items():
    # remaining volume in base currency
    volume = D(o['vol']) - D(o['vol_exec'])

    # extract for less typing
    descr = o['descr']

    # order price
    price = D(descr['price'])

    pair = descr['pair']
    base = pair[:3]
    quote = pair[3:]

    type_ = descr['type']
    if type_ == 'buy':
        # buying for quote - reduce quote balance
        balance[quote] -= volume * price
    elif type_ == 'sell':
        # selling base - reduce base balance
        balance[base] -= volume

for k, v in balance.items():
    # convert to string for printing
    if v == D('0'):
        s = '0'
    else:
        s = str(v)
    # remove trailing zeros (remnant of being decimal)
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    #
    print(k, s)
