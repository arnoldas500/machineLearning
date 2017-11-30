#sending sms using python script
#will need to pip install twillo
#my number: +16314961619
'''
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "ACXXXXXXXXXXXXXXXXX"
auth_token = "YYYYYYYYYYYYYYYYYY"

client = Client(account_sid, auth_token)

client.api.account.messages.create(
    to="+12316851234",
    from_="+15555555555",
    body="Hello there!")

'''

'''
#need to install
#pip isntall pybitcointools
#pip install bitcoin
from bitcoin import *

priv = random_key()
#print(prive)

pub = privtopub(priv)
#public bitcoin address addr
addr = pubtoaddr(pub)
'''

'''
#https://blockchain.info/ticker
#"USD" : {"15m" : 9619.39, "last" : 9619.39, "buy" : 9624.54, "sell" : 9614.24, "symbol" : "$"},
import time
import json
import urllib
from urllib.request import urlopen
from time import gmtime, strftime
import codecs

def main():
    
    reader = codecs.getreader("utf-8")
    btcPrices = urlopen('https://blockchain.info/ticker')
    #print(btcPrices)
    btcJson = json.load(reader(btcPrices))
    #last is the cur market price or last seen market price by the blockchain
    btcLast = btcJson['USD']['last']
    print("BTC price in USD last: ",btcLast)
    btc15 = btcJson['USD']['15m']
    print("BTC price in USD 15m ago: ", btc15)
    btcBuy = btcJson['USD']['buy']
    #print(btcBuy)
    #print the current time in python
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(time)

while True:
    main()
    #sleep for 1 sec since streaming prices and dont want to over ping the blockchain api
    time.sleep(1)
'''

import gdax
from time import gmtime, strftime
public_client = gdax.PublicClient()

products = public_client.get_products()
# Get the order book at the default level.
public_client.get_product_order_book('BTC-USD')
# Get the order book at a specific level.
public_client.get_product_order_book('BTC-USD', level=1)
# Get the product ticker for a specific product.
tickerBTC = public_client.get_product_ticker(product_id='BTC-USD')
tickerETH = public_client.get_product_ticker(product_id='ETH-USD')
tickerLTC = public_client.get_product_ticker(product_id='LTC-USD')

#historic rates
histRate = public_client.get_product_historic_rates('ETH-USD')

day = public_client.get_product_24hr_stats('BTC-USD')

#daily % change or daily move
#df['PCT_change'] = (df['Close'] - df['Open'] ) / df['Open'] * 100.0
pctChange = (float(day['last']) - float(day['open']) ) / float(day['open']) * 100

#print(day['PCT_change'])
print('open ',day['open'])
print('last ',day['last'])
print('high ',day['high'])
print('low ',day['low'])
time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print(time)
print("change up to current time from start of day",pctChange)
