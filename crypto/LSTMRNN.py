'''
price prediction of crypto currency using a long short term memory recurrent neural network
'''
#note: want to experment using mid instead of open andd ask instead of open or mid
'''
EX data sample
Header: Date	Open	High	Low	Close	Volume
Values: 2-Aug-17 318.94	327.12	311.22	325.89	13091462
Test2:
crypto currency diff from regular stocks, have last price rather then closing price since essentially the market never closes
Date          High     Low        Mid      Last        Volume
2014-04-15  513.9000  452.00  504.23500  505.0000   21013.584774
2014-04-16  537.50000  547.0000  495.00  538.0000  29633.358705
'''

import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import quandl
import matplotlib.pyplot as plt

#reading in the data
#bitcoinDF = pd.read_csv()
#getting the data set from quandle for free bitfinex/btcusd dataset                                                                             
bitcoinDF = quandl.get("BITFINEX/BTCUSD", authtoken="qeJmy9tSZu3gY3XdNoZs")

#make the date from an index into a column
bitcoinDF.reset_index(level=0, inplace=True)

print(bitcoinDF.head())

#get these specific columns from the dataset  
bitcoinDF = bitcoinDF[['Date','Mid' ,'High' ,'Low' ,'Last', 'Volume']]

print(bitcoinDF.head())

dates = bitcoinDF['Last'].values

print("Num days in bitcoin DF: {}".format(len(dates)))

#data preprocessing
#scaling data
scaler = StandardScaler()
scaledDF = scaler.fit_transform(dates.reshape(-1, 1))

#plot
plt.figure(figsize=(12,7), frameon=False, facecolor='brown', edgecolor='blue')
plt.title('Scaled bitcoin data from 2014/04/15 to current date')
plt.xlabel('Days')
plt.ylabel('Scaled value of bitcoin price')
plt.plot(scaledDF, label='bitcoin data')
plt.legend()
#plt.show()

#seperate features and labels
def windowData(data, windowSize):
    X = []
    y = []
    i = 0
    
    while (i + windowSize) <= len(data) -1:
        X.append(data[i:i + windowSize])
        y.append(data[i + windowSize])
        i+=1

    assert len(X) == len(y)
    return X, y

#windowing the dataset
X, y = windowData(scaledDF, 7)

#creating training and testing sets by holding out a portion of the data set
#first 1000 points of data for training
X_train = np.array(X[:1000]) #look up if i can specify a percetn to hold out **note**
y_train = np.array(y[:1000])

#last 15% of data for testing
X_test = np.array(X[1000:])
y_test = np.array(y[1000:])

print("X_train size: {}".format(X_train.shape))
print("y_train size: {}".format(y_train.shape))
print("X_test size: {}".format(X_test.shape))
print("y_test size: {}".format(y_test.shape))

#creating the recurrent neural network
'''
epoch = one forward pass and one backward pass of all the training examples
batch size = the number of training examples in one forward/backward pass
'''
epoches = 200
batchSize = 7

def lstm(hiddenLayerSize, batchSize, numLayers, dropout=True, dropoutRate=0.8):
    layer = tf.contrib.rnn.BasicLSTMCell(hiddenLayerSize)

    if dropout:
        layer = tf.contrib.rnn.DropoutWrapper(layer, output_keep_prob=dropoutRate)

    cell = tf.contrib.rnn.MultiRNNCell([layer]*numLayers)

    #initial state
    zeroState = cell.zero_state(batchSize, tf.float32)

    return cell, zeroState

def outputLayer(lstmOutput, inSize, outSize):
    X = lstmOutput[:, -1, :]
    print(X)

    weights = tf.Variable(tf.truncated_normal([inSize, outSize], stddev = 0.05), name='outputLayerWeights')

    bias = tf.Variable(tf.zeros([outSize]), name='outputLayerBias')

    #add bias so data wouldnt get screwd up during network if zero value or similar goes in
    output = tf.matmul(X, weights) + bias
    return output

def optLoss(logits, targets, learningRate, gradClipMargin):
    
    losses = []
    for i in range(targets.get_shape()[0]):
        losses.append([(tf.pow(logits[i] - targets[i], 2))])
        
    loss = tf.reduce_sum(losses)/(2*batchSize)
    
    #Cliping the gradient loss
    gradients = tf.gradients(loss, tf.trainable_variables())
    clipper_, _ = tf.clip_by_global_norm(gradients, gradClipMargin)
    optimizer = tf.train.AdamOptimizer(learningRate)
    trainOptimizer = optimizer.apply_gradients(zip(gradients, tf.trainable_variables()))
    return loss, trainOptimizer

class StockPredictionRNN(object):
    
    def __init__(self, learningRate=0.001, batchSize=7, hiddenLayerSize=512, numLayers=1, 
                 dropout=True, dropoutRate=0.8, numClasses=1, gradientClipMargin=4, windowSize=7):
    
        self.inputs = tf.placeholder(tf.float32, [batchSize, windowSize, 1], name='input_data')
        self.targets = tf.placeholder(tf.float32, [batchSize, 1], name='targets')

        cell, zeroState = lstm(hiddenLayerSize, batchSize, numLayers, dropout, dropoutRate)

        outputs, states = tf.nn.dynamic_rnn(cell, self.inputs, initial_state=zeroState)

        self.logits = outputLayer(outputs, hiddenLayerSize, numClasses)

        self.loss, self.opt = optLoss(self.logits, self.targets, learningRate, gradientClipMargin)

tf.reset_default_graph()
model = StockPredictionRNN()
