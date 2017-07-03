#!/usr/bin/env python3
# To debug historic OHLC data inconcistencies, as discussed here:
# https://www.reddit.com/r/kraken_traders/comments/6f6e9h/krakenapi_delivering_inconsistent_false_ohlc_data/

import decimal
import time

import krakenex

pair = 'XETHZEUR'
# UTC 2017-06-04 06:07:00, try: date '+%Y-%m-%d %H:%M:%S' -d '@TIMESTAMP' -u
timestamp = str(1496556420)

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
    ret = k.query_public('OHLC', req = {'pair': pair, 'since': timestamp})
    after = now()

    for i in range(5):
        print(ret['result'][pair][i])

    lineprint(after - before)

    time.sleep(20)
