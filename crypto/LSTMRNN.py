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
#training model by using prvious data and showing what the next days price is
#in this example i am using the last 7 days prices to show what the next days price is going to be

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

#get these specific columns from the dataset  (irrelewent right now)
bitcoinDF = bitcoinDF[['Date','Mid' ,'High' ,'Low' ,'Last', 'Volume']]

print(bitcoinDF.head())

#only taking closeing or last price into the model, each value represents each day starting from 2014, 04, 15
curData = bitcoinDF['Last'].values

#print(curData) [  505.    538.    508.  ...,  7321.8  6956.5  7102. ]

print("Num days in bitcoin DF: {}".format(len(curData)))

#data preprocessing
#scaling data
scaler = StandardScaler()
scaledDF = scaler.fit_transform(curData.reshape(-1, 1))

#plot
plt.figure(figsize=(12,7), frameon=False, facecolor='brown', edgecolor='blue')
plt.title('Scaled bitcoin data from 2014/04/15 to current date')
plt.xlabel('Days')
plt.ylabel('Scaled value of bitcoin price')
plt.plot(scaledDF, label='bitcoin data')
plt.legend()
#plt.show()

#note double dhcekc ***
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
X, y = windowData(scaledDF, 7) #second number is how many previous days prices we should use for prediction

#creating training and testing sets by holding out a portion of the data set
#first 1000 points of data for training
X_train = np.array(X[:1200]) #look up if i can specify a percetn to hold out **note**
y_train = np.array(y[:1200])

#last 15% of data for testing
X_test = np.array(X[1200:])
y_test = np.array(y[1200:])

print("X_train size: {}".format(X_train.shape))
print("y_train size: {}".format(y_train.shape))
print("X_test size: {}".format(X_test.shape))
print("y_test size: {}".format(y_test.shape))

#creating the recurrent neural network
'''
epoch = one forward pass and one backward pass of all the training examples
batch size = the number of training examples in one forward/backward pass
'''
epoches = 1 #try 200
batchSize = 7 #try 7

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

class StockPredictionRNN(object): #change batch size and window size to 7
    
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


#taining the model
session = tf.Session()
session.run(tf.global_variables_initializer())

for i in range(epoches):
    trainedScores = []
    ii=0
    epochLoss = []
    while(ii + batchSize) <= len(X_train):
        X_batch = X_train[ii:ii+batchSize]
        y_batch = y_train[ii:ii+batchSize]

        o, classification, _ = session.run([model.logits, model.loss, model.opt], feed_dict={model.inputs:X_batch, model.targets:y_batch})

        epochLoss.append(classification)
        trainedScores.append(o)
        ii += batchSize
    if(i % 30) == 0:
        #show loss at every 30 increments (or epoches)
        print('Epoch {}/{}'.format(i, epoches), ' Current loss: {}'.format(np.mean(epochLoss)))


sup =[]
for i in range(len(trainedScores)):
    for j in range(len(trainedScores[i])):
        sup.append(trainedScores[i][j])

tests = []
i = 0

#print(X_test) values from -1 to 5
#print(y_test)

while i+batchSize <= len(X_test):
    
    o = session.run([model.logits], feed_dict={model.inputs:X_test[i:i+batchSize]})
    #print(o) predictions
    i += batchSize
    tests.append(o)
print(len(tests))

testsNew = []
for i in range(len(tests)):
    for j in range(len(tests[i][0])):
        testsNew.append(tests[i][0][j])

print(len(testsNew))

testResults = []
for i in range(1267): #1266
    if i >= 1204: #1001 when training on 1000 data points #1105 when training on 1100 
        testResults.append(testsNew[i-1204])
    else:
        testResults.append(None)

#plotting predictions from the model
plt.figure(figsize=(16, 7))
plt.title('Scaled bitcoin data from 2014/04/15 to current date')
plt.plot(scaledDF, label='Original data')
plt.plot(sup, label='Training data')
plt.plot(testResults, label='Testing data/ predictions')
plt.legend()
plt.show()

session.close()
