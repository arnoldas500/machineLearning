import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')
'''
#can specify start and end dates
start = dt.datetime(2000,1,1)
end = dt.datetime(2016,12,31)
#data from yahoo finance api for tesla stock
df = web.DataReader('TSLA', 'yahoo', start, end)

#reading a csv in of your own
df = pd.read_csv('filename', parse_dates=True, index_col=0);
#giving it a date time index by doing parse_dates=True, index_col=0
print(df.head())
#will graph for you and give you a legend
df.plot()
plt.show()

#if you want to plot something very specific you can reference the specific columns in pandas
df['Adj. Close'].plot()
print(df[['Open','Close']].head())
'''
#can specify start and end dates                                                                                                                         
start = dt.datetime(2000,1,1)                                                                                                                            
end = dt.datetime(2016,12,31)                                                                                                                            
#data from yahoo finance api for tesla stock                                                                                                             
df = web.DataReader('TSLA', 'yahoo', start, end) 


#df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
#creating our own col in the data frame called 100 moving avg (takes todays price and 99 of prev close price and takes the avg of them)
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
print(df.head())

#6,1 is 6 by 1 and starting at 0,0
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
#sharex=ax1 makes both the plots share an x axis so when you zoom in on one the other will also zoom in accordingly
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

#plots a line which takes in x and y , x = df.index and y = ajd close
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()
