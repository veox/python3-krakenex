# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 19:21:28 2017

@author: Sémy Mechaab

 Prints the account balance and will in future send it via email,
 with obvisouly your own email adress (SOON).
 
 Please fill and copy your kraken.key file in the same directory.
 
 If you have any questions or suggestions, please email me at 
 s.mechaab@gmail.com.
 
 Please, don't hesitate to feedback !
 
v0.1
1. Displays the different amount of crypto currencies you own on your Kraken wallet.
2. Displays the total crypto money you own in equivalent fiat money.
3. Adapted to the crypto and fiat currencies you already own.
4. If you don't own any fiat money on your Kraken wallet, it will be displayed the equivalent in USD.
(The fiat money can be easily modified but be aware that some markets doesn't allow it,
DASHUSD -> DASHJPY for example, can't be done because the market doesn't exist on Kraken.
Check k.query_public('Ticker',{'pair': 'YOURMARKET',}) inline to know if it exist.)
5. Works with multi-fiat currencies wallets.

 
"""
#%% Includes
import krakenex
import re
import sys

currencies = [] #List of differents currencies owned by client
market = []     #List of actual market currency owned by client
balance = []    #List of the actual market balance of crypto currencies

#%%Extracting data from Kraken Exchange API
k = krakenex.API()
k.load_key('kraken.key')    
data = k.query_private('Balance')
#print(data)
#TODO if error
data = str(data['result'])

#DEBUG
data = data.replace("XXRP","ZUSD")
#Can be used to test if others currencies (e.g ZPJY) are compatibles with others market pairs you are into. 

#%%We find currencies concerned by the client wallet
#crypto_index = []

#Exctracts crypto currencies
crypto_index = [m.start() for m in re.finditer("'X", data)]
#print (crypto_index)
if crypto_index == [] : sys.exit("Can't find any crypto currency on your wallet yet.")
for i in crypto_index:
    currencies.append(data[i+1:i+5])

#Extracts crypto currencies beginning with 'D' (they are 4 letters long currencies today:\
#DASH and DOGE)
crypto_index_tmp = [m.start() for m in re.finditer("'D", data)]
for i in range(len(crypto_index_tmp)):
    crypto_index.append(crypto_index_tmp[i])
#print (crypto_index)
for i in crypto_index_tmp:
    currencies.append(data[i+1:i+5])
    
#Extracts fiat currencies
fiat_index = [m.start() for m in re.finditer("'Z", data)]
#print (fiat_index)

for i in fiat_index:
    currencies.append(data[i+1:i+5])
if fiat_index == [] :
    print("Currencies will be converted in USD by default")
    fiat_index.append(0)
    currencies.append('ZUSD')

print("Currencies on your wallet : ",currencies)

#%%We prepare our list of markets exchange we are interested in
for i in range(len(crypto_index)):
    for j in range(len(fiat_index)):
        if currencies[i][0]=='D':
            market.append(currencies[i][0:4]+currencies[len(crypto_index)+j][1:4])
        else :
            market.append(currencies[i][1:4]+currencies[len(crypto_index)+j][1:4])
        
print("Markets we aim to analyze to : ",market) #This is optionnal
#Add more currencies if needed but it's done automatically

#%%Here we get our current currency situation
#raw currency values to be extracted

for i in range(len(crypto_index)):
    balance.append(data[crypto_index[i]+9:crypto_index[i]+17])
    
if(fiat_index[0] != 0):
    for i in range(len(fiat_index)):
        balance.append(data[fiat_index[i]+9:fiat_index[i]+15])
else:
    balance.append('0')
#We extract what we need

#%% Converting balance to float (needed for operations)
for i in range(len(currencies)): # +1 to count EUR in casting str->float
    balance[i] = float(balance[i])
print("Current balance you own : ",balance)
#Casting current balance to float

#%% Extracts price of every currencies client is involved onto
price = []

for i in range(len(market)):
    data_price = k.query_public('Ticker',{'pair': market[i],})
    #print(data_price)
    #We extract 
    indx = str(data_price['result']).find('c')
    price.append(str(data_price['result'])[indx+6:indx+15])
    
    price[i] = float(price[i])
    #price is a list of str -> cast to float
#%% Finally multiplying balance of crypto of client wallet BY actual real-time price of market
# price of coin in FIAT * amount of coin = Estimated value of currencies in FIAT MONEY
values = {}
total = {}
totals = []
for i in fiat_index:
    total.update({data[i+1:i+5] : ''})
    totals.append(0)
#Initializing in case we never get the market data


#Cross converting data from each fiat to their corresponding market (ZEUR with XBTEUR, ETHEUR,... \
# same for ZUSD and XBTUSD, ETHUSD, etc...)
for n in range(len(fiat_index)):   
    for i in range(len(currencies)-len(fiat_index)):
        if i-n < 0 : 
            values.update({market[i*len(fiat_index)-n] : price[i*len(fiat_index)-n] * balance[len(balance)-len(fiat_index)-1]})
        else: 
            values.update({market[i*len(fiat_index)-n] : price[i*len(fiat_index)-n] * balance[i-n]})       
            
        totals[n] += values[market[i*len(fiat_index)-n]]
    values.update({currencies[len(crypto_index)+n] : balance[len(crypto_index)+n]})
#For each market, we calculate the price for each fiat money involved in
#One exception : when i-n < 0, we need to fix balance index because 
#len(price) and len(market) is not equal to len(balance)        
    
    totals[n] += balance[len(crypto_index)+n] 
# Don't forget to add what is remaining in fiat in your wallet

#%% Displaying
for i in range(len(fiat_index)):
    total.update({list(total.keys())[i] : totals[i]})      
        

values.update({'Total' : total})
print(values)
#We could store our data in a dict type
