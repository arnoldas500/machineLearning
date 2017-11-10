import bs4 as bs
#beutifulsoup is a web scraping library
#pickle seriealizies any object
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import fix_yahoo_finance 
import time

#s&p 500 is the top 500 companies by market cap
#market cap is the value of that company over the number of outstanding shares times the price
'''
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
'''
#save_sp500_tickers()

#updated
def save_sp500_tickers():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table",{"class":"wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        mapping = str.maketrans(".","-")
        ticker = ticker.translate(mapping)
        tickers.append(ticker)
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        print(tickers)
    return tickers


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
        print(ticker)
        #yahoo starts throttling so need to add time.sleep
        #time.sleep(0.9)
        # just in case your connection breaks, we'd like to save our progress!
        #if the csv file for that day doesnt exist we are going to grab it
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            #df = web.DataReader(ticker, "yahoo", start, end)
            #df = web.get_data_yahoo(ticker, start, end)
            df = download(ticker, start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
    '''

#save_sp500_tickers()
get_data_from_yahoo()


def get_data_goog(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start=dt.datetime(2000,1,1)
    end=dt.datetime(2016,12,31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'google', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}',format(ticker))
            
#get_data_goog()

def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close':ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


#compile_data()
