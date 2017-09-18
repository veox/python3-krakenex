#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# To debug historic OHLC data inconcistencies, as discussed here:
# https://www.reddit.com/r/kraken_traders/comments/6f6e9h/krakenapi_delivering_inconsistent_false_ohlc_data/

import krakenex

import decimal
import time

pair = 'XETHZEUR'
# NOTE: for the (default) 1-minute granularity, the API seems to provide
# data up to 12 hours old only!
since = str(1499000000) # UTC 2017-07-02 12:53:20

k = krakenex.API()

def now():
    return decimal.Decimal(time.time())

def lineprint(msg, targetlen = 72):
    line = '-'*5 + ' '
    line += str(msg)

    l = len(line)
    if l < targetlen:
        trail = ' ' + '-'*(targetlen-l-1)
        line += trail

    print(line)
    return

while True:
    lineprint(now())

    before = now()
    ret = k.query_public('OHLC', data = {'pair': pair, 'since': since})
    after = now()

    # comment out to track the same "since"
    #since = ret['result']['last']

    # TODO: don't repeat-print if list too short
    bars = ret['result'][pair]
    for b in bars[:5]: print(b)
    print('...')
    for b in bars[-5:]: print(b)

    lineprint(after - before)

    time.sleep(20)
