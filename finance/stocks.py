import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

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


'''
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
'''

#doing some resampling and candlestick plots
#lets say you collect data every min or whatever, but you need hourly data, then you can resample to be hourly data from min data
#resample from daily data to 10 day data can do .mean ect we are using .ohlc=open high low close
df_ohlc = df['Adj Close'].resample('10D').ohlc()
#taking sum over 10 days of vol
df_volume = df['Volume'].resample('10D').sum()

#can get all of the values of a datafram by doing df.values
#reseting index so date is now a column
df_ohlc.reset_index(inplace=True)
#convert the date to mdates since thats what matplotlib uses (dont know why)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num) #map just maps this onto every date to convert from date to mdates object

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

#where the candle stick is filled in shows the open and close low and high
candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
#fills from 0 to vol high on second plot
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
