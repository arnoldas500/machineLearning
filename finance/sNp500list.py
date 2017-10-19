import bs4 as bs
#beutifulsoup is a web scraping library
#pickle seriealizies any object
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web


#s&p 500 is the top 500 companies by market cap
#market cap is the value of that company over the number of outstanding shares times the price
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers

#save_sp500_tickers()


def get_data_from_yahoo(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)

    #taking the datasets and storing them in there own folders
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)
    
    #to grab all the data, can also speify tickers[:125] to grab from 0 to the first 125 or whatever
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        #if the csv file for that day doesnt exist we are going to grab it
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "yahoo", start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data_from_yahoo()
