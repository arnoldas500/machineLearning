import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
#svm is a support vector machine
from sklearn.linear_model import LinearRegression
#getting the data set from quandle for free sick wiki dataset
df = quandl.get('WIKI/GOOGL') 
#each column is a feature EX: open high low close ...
print(df.head())

#get these specific columns from the dataset
df = df[['Adj. Open' ,'Adj. High' ,'Adj. Low' ,'Adj. Close' ,'Adj. Volume']]

#the margin of high and low tells us a little bit about the volitility for the day
#the open price for the day compared to the close price of the day tells us if the price went up or
#if the price went down for the day

#high - low % or % volitility for day
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close'] ) / df['Adj. Close'] * 100.0

#daily % change or daily move
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open'] ) / df['Adj. Open'] * 100.0

#our new dataframe with data that we calculated 
#volume is how many trades occured in one day
df = df [[ 'Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume' ]]

#features are the attributes that make up the label 
#labels are prediction into the future 
#print(df.head())

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True) # fill any empty spots with -99999

#number of days out for how many days we are predicting (0.01 for 01% out)
forecast_out = int(math.ceil(0.01*len(df)))
print(forecast_out)

#shifting the columns negatively so each row will be adjusted close price for 10 days into the future
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)
#print(df.head())

#features are a capital X
X= np.array(df.drop(['label'],1))
#labels are lowercase y
y= np.array(df['label'])

X = preprocessing.scale(X)

#X = X[:-forecast_out+1]
#df.dropna(inplace=True)
y = np.array(df['label'])

print(len(X),len(y))

#going to use 20%, takes all our features and labels and shuffels them up but keeping x and y connected
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)


#clf is a clasifier
clfLR = LinearRegression()
clfLR.fit(X_train, y_train)

accuracyLR = clfLR.score(X_test, y_test)

print("Linear regression test: %f"%accuracyLR)

clfSVM = svm.SVR() 
clfSVM.fit(X_train, y_train)
accuracySVM = clfSVM.score(X_test, y_test)

print("support vector machine: %f" %accuracySVM)
