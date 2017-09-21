#!/usr/bin/env python

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Kraken bitcoin exchange (Payward, Inc.) United States IRS tax compliance script
# Generate 2016 Sales and Other Dispositions of Capital Assets
# Form 8949 spreadsheet (OMB No. 1545-0074)
#
# WARNING: submits a lot of queries in rapid succession!

# Maintainer: Austin.Deric@gmail.com (@AustinDeric on github)

import pandas as pd
import krakenex

import datetime
import calendar
import time

# takes date and returns nix time
def date_nix(str_date):
    return calendar.timegm(str_date.timetuple())

# takes nix time and returns date
def date_str(nix_time):
    return datetime.datetime.fromtimestamp(nix_time).strftime('%m, %d, %Y')

# return formated Trades History request data
def data(start, end, ofs):
    req_data = {'type': 'all',
                'trades': 'true',
                'start': str(date_nix(start)),
                'end': str(date_nix(end)),
                'ofs': str(ofs)
                }
    return req_data

k = krakenex.API()
k.load_key('kraken.key')

data = []
count = 0
#the maximum r
for i in range(6,11):
    start_date = datetime.datetime(2016, i+1, 1)
    end_date = datetime.datetime(2016, i+2, 29)
    th = k.query_private('TradesHistory', data(start_date, end_date, 1))
    print(th['error'])
    time.sleep(.1)
    print(th)
    th_error = th['error']
    if int(th['result']['count'])>0:
        count += th['result']['count']
        data.append(pd.DataFrame.from_dict(th['result']['trades']).transpose())

#
trades = pd.concat(data, axis = 0)
trades = trades[~trades.index.duplicated()]
trades = trades.sort(columns='time', ascending=True)
trades.to_csv('data.csv')

#format pair description for IRS
trades.ix[trades.pair == 'XXBTZUSD', 'pair'] = 'XBT/USD cryptocurrency'
trades.ix[trades.pair == 'XETHZUSD', 'pair'] = 'ETH/USD cryptocurrency'
trades.ix[trades.pair == 'XETHXXBT', 'pair'] = 'ETH/XBT cryptocurrency'
trades.ix[trades.pair == 'XDAOXXBT', 'pair'] = 'DAO/XBT cryptocurrency'

#rowi is the opening position
net = 0.0
line_items = []
count =0
total_proceeds = 0
total_cost = 0
total_net = 0
for i,rowi in trades.iterrows():
    if rowi['posstatus']=='closed':
        for j in rowi['trades']:
            #rowk is a closing trade
            for k, rowk in trades.iterrows():
                if j == k:
                    cost = float(rowi['cost']) + float(rowi['fee'])
                    total_cost += cost
                    proceeds = float(rowi['ccost']) - float(rowi['cfee'])
                    total_proceeds += proceeds
                    total_net += float(rowi['net'])
                    line_item = {'1(a) Description of property': str(rowi['vol']) + " " + rowi['pair'],
                                 '1(b) Date aquired': date_str(rowi['time']),
                                 '1(c) Date sold or disposed of':date_str(rowk['time']),
                                 '1(d) Proceeds': proceeds,
                                 '1(e) Cost or other basis.': cost,
                                 '1(h) Gain or (loss).': float(rowi['net'])
                    }
                    line_items.append(pd.DataFrame(line_item, index=[count]))
                    count += 1

form8949 = pd.concat(line_items, axis=0)
print('form8949: ')
print(form8949)
print('2(d) Totals. Proceeds ' + str(total_proceeds))
print('2(e) Totals. Cost or other basis. ' + str(total_cost))
print('2(h) Gain or (loss). ' + str(total_net))
form8949.to_csv('form8949.csv')
