import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import fix_yahoo_finance

df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
df.columns = df.ix[0]
df.drop(df.index[0], inplace=True)
tickers = df['Ticker symbol'].tolist()


def get_data_from_yahoo():
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2017, 6, 29)

    for ticker in tickers:
        if not os.path.exists("stock_dfs/{}.csv".format(ticker)):
            #df = web.DataReader(ticker,"quandl",start,end)
            try:
                df = web.get_data_yahoo(ticker,start,end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except: 
                print('Cannot obtain data for ' +ticker+" with yahoo")
                print("Trying with google : ")
                try :
                    df = web.DataReader(ticker,"google",start,end)
                    df.to_csv('stock_dfs/{}.csv'.format(ticker))
                except:
                    print("still not working ! added to notworking pickle")
                
                    bad_tickers.append(ticker)
                    with open("notworking.pickle","wb") as u:
                        pickle.dump(bad_tickers,u)
                
        else:
            print('Already have {}'.format(ticker))
    '''
    for ticker in tickers:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            list = pdr.get_data_yahoo(ticker, start, end)
            list.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
    '''
get_data_from_yahoo()
