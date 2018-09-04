#!/usr/bin/env python

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# FIXME: Prints the sum of _some_ open positions?..

# Maintainer: Austin.Deric@gmail.com (@AustinDeric on github)

import krakenex

# configure api
k = krakenex.API()
k.load_key('kraken.key')

# prepare request
req_data = {'docalcs': 'true'}

# query servers
start = k.query_public('Time')
open_positions = k.query_private('OpenPositions', req_data)
end = k.query_public('Time')
latency = end['result']['unixtime'] - start['result']['unixtime']

# parse result
b, c = 0, 0

for order in open_positions['result']:
    coin = order["pair"]
    if coin == 'XETHZUSD':
        b += (float(order['vol']))
    elif coin == 'XXBTZUSD':
        c += (float(order['vol']))

n_errors = len(open_positions['error'])
total = len(open_positions['result'])

msg = """
error counts: {n_errors}
latency: {latency}

open orders
    eth: {b}
    btc: {c}
    total: {total}
"""
print(msg.format(n_errors=n_errors, total=total, b=b, c=c, latency=latency))
