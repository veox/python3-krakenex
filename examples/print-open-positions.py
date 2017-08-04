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

# querry servers
start = k.query_public('Time')
open_positions = k.query_private('OpenPositions', req_data)
end = k.query_public('Time')
latency = end['result']['unixtime']-start['result']['unixtime']

# parse result
dict(open_positions)

b = 0
c = 0
for i in open_positions['result']:
    order = open_positions['result'][i]
    if(order['pair']=='XETHZUSD'):
        b += (float(order['vol']))
    if (order['pair'] == 'XXBTZUSD'):
        c += (float(order['vol']))

print('error count: ' + str(len(open_positions['error'])))
print('latency: ' + str(latency))
print('total open eth: ' + str(b))
print('total open btc: ' + str(c))
print('total open positions: ' + str(len(open_positions['result'])))
