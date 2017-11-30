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

#https://blockchain.info/ticker
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
    btcBuy = btcJson['USD']['buy']
    print(btcBuy)
    #print the current time in python
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(time)

while True:
    main()
    #sleep for 1 sec since streaming prices and dont want to over ping the blockchain api
    time.sleep(1)
