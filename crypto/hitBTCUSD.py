#run source py3/bin/activate to activate correct python env to run this file
'''
C-a
Move to the beginning of the line (beginning-of-line).
C-e
Move to the end of the line (end-of-line).
M-f
Move forward one word (forward-word).
M-b
Move backward one word (backward-word).
'''


import pandas as pd
import quandl
import math, datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
import matplotlib.pyplot as plt
from matplotlib import style
#import bestFitSlope as bfs
#picking is a good thing to have to save time when doing seralization of a classifier
import pickle

style.use('ggplot')

#svm is a support vector machine
from sklearn.linear_model import LinearRegression
#getting the data set from quandle for hitBTCUSD dataset with good OHLCV data since 2013-12-27
df = quandl.get("BCHARTS/HITBTCUSD", authtoken="qeJmy9tSZu3gY3XdNoZs") 
#each column is a feature EX: open high low close ...
print(df.head())

#get these specific columns from the dataset
df = df[['Open' ,'High' ,'Low' ,'Close' ,'Volume (Currency)']]

#the margin of high and low tells us a little bit about the volitility for the day
#the open price for the day compared to the close price of the day tells us if the price went up or
#if the price went down for the day

#high - low % or % volitility for day
df['HL_PCT'] = (df['High'] - df['Close'] ) / df['Close'] * 100.0

#daily % change or daily move
df['PCT_change'] = (df['Close'] - df['Open'] ) / df['Open'] * 100.0

#our new dataframe with data that we calculated 
#volume is how many trades occured in one day
df = df [[ 'Close', 'HL_PCT', 'PCT_change', 'Volume (Currency)' ]]

#features are the attributes that make up the label 
#labels are prediction into the future 
#print(df.head())       

forecast_col = 'Close'
df.fillna(-99999, inplace=True) # fill any empty spots with -99999

#number of days out for how many days we are predicting (0.1 for 10% out)
forecast_out = int(math.ceil(0.05*len(df)))
print("number of days we are predicting %d" %forecast_out)

#shifting the columns negatively so each row will be adjusted close price for days into the future
df['label'] = df[forecast_col].shift(-forecast_out)
#df.dropna(inplace=True)
#print(df.head())

#features are a capital X
X = np.array(df.drop(['label'],1))
#print(X)
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
#x first is 90% of data
X = X[:-forecast_out]


#labels are lowercase y
#y= np.array(df['label'])



df.dropna(inplace=True) 
y = np.array(df['label'])


print(len(X),len(y))

#going to use 20%, takes all our features and labels and shuffels them up but keeping x and y connected
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#****Could comment out below because the pcikle is saved and dont have to retrain****
#clf is a clasifier
#n_jobs is how many threads we want to use per batch (-1 runs as many as it can by your cpu)
clfLR = LinearRegression(n_jobs=10)
clfLR.fit(X_train, y_train)
#can save the training so you dont have to train it everytime
with open('linearregression.pickle','wb') as f:
    pickle.dump(clfLR, f)
#***can comment out till here if using pickle saved in local dir*** (pickle data is the classifier)

pickle_in = open('linearregression.pickle','rb')
clfLR = pickle.load(pickle_in) #load it in

accuracyLR = clfLR.score(X_test, y_test)

print("Linear regression test: %f"%accuracyLR)


clfSVM = svm.SVR() 
clfSVM.fit(X_train, y_train)
accuracySVM = clfSVM.score(X_test, y_test)

print("support vector machine: %f" %accuracySVM)

#doing a prediction
forecast_set = clfLR.predict(X_lately)
print(forecast_set, accuracyLR, forecast_out)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    #df.loc next_date is a date stamp which is the index of the dataframe
    df.loc[next_date] = [np.nan for _ in range(len(df.columns) -1)] + [i]

df['Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

#picking is saving your classifier so you dont have to retrain it everytime you run your program
#load it in without any training time
