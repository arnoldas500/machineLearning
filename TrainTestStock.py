import pandas as pd
import quandl
import math

#getting the data set from quandle for free sick wiki dataset
df = Quandl.get('WIKI/GOOGL') 
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
print(df.head())

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True) # fill any empty spots with -99999

#number of days out for how many days we are predicting (0.01 for 01% out)
forcast_out = int(math.ceil(0.01*len(df)))

#shifting the columns negatively so each row will be adjusted close price for 10 days into the future
df['label'] = df[forecast_col].shift(-forecast_out)

print(df.head())
