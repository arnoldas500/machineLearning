'''
price prediction of crypto currency using a long short term memory recurrent neural network
'''

'''
EX data sample
Header: Date	Open	High	Low	Close	Volume
Values: 2-Aug-17 318.94	327.12	311.22	325.89	13091462
Test2:
Date          High     Low        Mid      Last        Volume
2014-04-15  513.9000  452.00  504.23500  505.0000   21013.584774
'''

import tensorflow as tf
import pandas as pd
import numpy as np
import sklearn
import quandl
import matplotlib.pyplot as plt

#read in the data
#bitcoinDF = pd.read_csv()
#getting the data set from quandle for free bitfinex/btcusd dataset                                                                             
bitcoinDF = quandl.get("BITFINEX/BTCUSD", authtoken="qeJmy9tSZu3gY3XdNoZs")

print(bitcoinDF.head())
