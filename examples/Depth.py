import krakenex

k = krakenex.API()

print(k.query_public('Depth',{'pair': 'XXBTZUSD', 'count': '10'}))
