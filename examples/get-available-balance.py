#!/usr/bin/env python

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Get balance available for trading/withdrawal (not on orders).
#
# NOTE: Assumes limit orders. Margin positions are not taken into account!
# NOTE: floating-point rounding errors not taken into account!
#
# FIXME: Also shows how current krakenex usage has too much sugar.

import krakenex
import pprint

k = krakenex.API()
k.load_key('kraken.key')

balance = k.query_private('Balance')
orders = k.query_private('OpenOrders')

balance = balance['result']
orders = orders['result']

newbalance = dict()
for currency in balance:
    # remove first symbol ('Z' or 'X')
    newname = currency[1:] if len(currency) == 4 else currency
    newbalance[newname] = float(balance[currency])
balance = newbalance

for _, o in orders['open'].items():
    # base volume
    volume = float(o['vol']) - float(o['vol_exec'])

    # extract for less typing
    descr = o['descr']

    # order price
    price = float(descr['price'])

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

pprint.pprint(balance)
