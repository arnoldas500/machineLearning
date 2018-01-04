#/usr/bin/env python
#sending sms using python script
#will need to pip install twillo
#my number: +16314961619
from twilio.rest import Client
import gdax
from time import gmtime, strftime
import time
import json
import urllib
from urllib.request import urlopen
import codecs
import sys

public_client = gdax.PublicClient()
account_sid = 
auth_token = 

client = Client(account_sid, auth_token)

comparePrice = 0
comparePriceETH = 0
comparePriceLTC = 0

def priceStore():
    global comparePriceETH
    global comparePriceLTC
    global comparePrice
    comparePriceETH = 0
    comparePriceLTC = 0
    comparePrice = 0

#setGlobPrice()

def gdax():


    #products = public_client.get_products()
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
    #pctChange = (float(day['last']) - float(day['open']) ) / float(day['open']) * 100



    dayETH = public_client.get_product_24hr_stats('ETH-USD')

    #daily % change or daily move
    #df['PCT_change'] = (df['Close'] - df['Open'] ) / df['Open'] * 100.0
    #pctChangeETH = (float(dayETH['last']) - float(dayETH['open']) ) / float(dayETH['open']) * 100





    dayLTC = public_client.get_product_24hr_stats('LTC-USD')

    #daily % change or daily move
    #df['PCT_change'] = (df['Close'] - df['Open'] ) / df['Open'] * 100.0
    #pctChangeLTC = (float(dayLTC['last']) - float(dayLTC['open']) ) / float(dayLTC['open']) * 100


    btcPass = True
    ethPass = True
    ltcPass = True
    time1 = time.time()
    #to get the diff time.time() - time1
    #seconds in 2 hours = 7200
    #changing from using time to send message
    #to if price changes from the last compare price at least 5% then send messgae

    global comparePriceETH
    global comparePriceLTC
    global comparePrice


    if(comparePrice == 0):
        #print("COMPARE PRICE NOT UPDATED ",comparePrice)
        pctChange = (float(day['last']) - float(day['open']) ) / float(day['open']) * 100
    else:
        print("compare change price updated ",comparePrice)
        pctChange = (float(day['last']) - float(comparePrice) ) / float(comparePrice) * 100

    if(comparePriceETH == 0):
         pctChangeETH = (float(dayETH['last']) - float(dayETH['open']) ) / float(dayETH['open']) * 100
    else:
         pctChangeETH = (float(dayETH['last']) - float(comparePriceETH) ) / float(comparePriceETH) * 100

    if(comparePriceLTC == 0):
         pctChangeLTC = (float(dayLTC['last']) - float(dayLTC['open']) ) / float(dayLTC['open']) * 100
         #check if key is not null then 
    else:
         pctChangeLTC = (float(dayLTC['last']) - float(comparePriceLTC) ) / float(comparePriceLTC) * 100



    #print(day['PCT_change'])
    # print('gdax exchange for BTC in USD')
    # print('open ',day['open'])
    # print('last ',day['last'])
    # print('high ',day['high'])
    # print('low ',day['low'])
    # timeB = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # print(timeB)
    # print("change up to current time from start of day ",pctChange)

    # #print(day['PCT_change'])
    # print('gdax exchange for ETH in USD')
    # print('open ',dayETH['open'])
    # print('last ',dayETH['last'])
    # print('high ',dayETH['high'])
    # print('low ',dayETH['low'])
    # timeE = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # print(timeE)
    # print("change up to current time from start of day",pctChangeETH)

    #  #print(day['PCT_change'])
    # print('gdax exchange for LTC in USD')
    # print('open ',dayLTC['open'])
    # print('last ',dayLTC['last'])
    # print('high ',dayLTC['high'])
    # print('low ',dayLTC['low'])
    # timeL = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # print(timeL)
    # print("change up to current time from start of day",pctChangeLTC)


    if(abs(pctChange)>5):
        if(btcPass):
            #btcPass = False
            

            print("about to send message for BTC change")
            client.api.account.messages.create(
                    to="+16317047013",
                    from_="+16314961619",
                    #body="BTC % change from last comparedPrice "+str(comparePrice)+" is "+str(pctChange)+"\n\n -Arnold")
                    body="gdax exchange for BTC in USD\n"+'last '+str(day['last'])+"\nBTC % change from last comparedPrice "+str(comparePrice)+" is %"+str(pctChange)+"\n\n -Arnold")
            comparePrice = float(day['last'])
    else:
        #btcPass = True
        pass


    '''
    if(btcPass):
        if(abs(pctChange)>5):
            #btcPass = False

            if((time.time() - last) > 7200 ):
                client.api.account.messages.create(
                    to="+16317047013",
                    from_="+16314961619",
    body="gdax exchange for BTC in USD\n"+'last '+str(day['last'])+"\nBTC % change from last comparedPrice "+comparePrice+" is "+str(pctChange)+"\n\n -Arnold")


    else:
        last = time.time()
    '''

    if(ethPass):
        if(abs(pctChangeETH)>5):
            #ethPass = False
            
            print("about to send message for ETH change")
            client.api.account.messages.create(
                to="+16317047013",
                from_="+16314961619",
                #body="ETH % change from last comparedPrice "+str(comparePriceETH)+" is "+str(pctChangeETH)+"\n\n -Arnold")
                body="gdax exchange for ETH in USD\n"+'last '+str(dayETH['last'])+"\nETH % change from last comparedPrice "+str(comparePriceETH)+" is %"+str(pctChangeETH)+"\n\n -Arnold")
            comparePriceETH = float(dayETH['last'])

    else:
        pass

    if(ltcPass):
        if(abs(pctChangeLTC)>5):
            
            print("about to send message for LTC change")
            #ltcPass = False
            client.api.account.messages.create(
                to="+16317047013",
                from_="+16314961619",
                #body="LTC % change from last comparedPrice "+str(comparePriceLTC)+" is "+str(pctChangeLTC)+"\n\n -Arnold")
                body="gdax exchange for LTC in USD\n"+'last '+str(dayLTC['last'])+"\nLTC % change from last comparedPrice "+str(comparePriceLTC)+" is %"+str(pctChangeLTC)+"\n\n -Arnold")
            comparePriceLTC = float(dayLTC['last'])

    else:
        pass

        


#run it

while(True):
    try:
        gdax()
    except Exception:
        continue
       



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


