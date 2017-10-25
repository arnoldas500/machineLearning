import tweepy
#from crds import *
import pandas as pd
from textblob import TextBlob
import time
from prettytable import PrettyTable
from datetime import datetime
#import sqlite3

#conn = sqlite3.connect('twitterprofiles.db')
#c = conn.cursor()

targettwitterprofile = 'Bitcoin'

#c.execute('CREATE TABLE '+targettwitterprofile+' (dbtweetid int PRIMARY KEY, dbtweetdate date, dbtweettext text, polarity real)')

consumer_key = 'E3xLP2DJVCojAuRc4dsIQhOhH'
consumer_secret = '46e1t5l5uZDUY3WfuNf0NwzsNVdPnJS7qtVjVc6HKwxfH0BYX4'

access_token = '398425873-SL80lXVpCqZN8zTTNWSz6pBWRdy1CwzdWQlRrBEu'
access_token_secret = 'FAmHxrdwJfnrcjRVKvuxVRpoQfezjS7npTc6dH20EfwAq'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#api = tweepy.API(auth,wait_on_rate_limit=True)
api = tweepy.API(auth)

df = pd.DataFrame() #creates a new dataframe that's empty

x = PrettyTable()
x.field_names = ["Count", "ID", "Date", "Text", "Polarity"]
cols = ["ID", "Date", "Polarity"]
n = 1
data = []

for page in tweepy.Cursor(api.user_timeline, id=targettwitterprofile, count=200).pages(20):
    for tweet in page:
        tweetid = tweet.id
        tweetdate = datetime.strptime(str(tweet.created_at)[:10],'%Y-%m-%d').strftime('%d-%m-%Y')
        tweettext = tweet.text
        polarity = round(TextBlob(tweettext).sentiment.polarity,4)
        x.add_row([n,tweetid, tweetdate, tweettext, polarity])
        #df['polarity'].append(polarity)
        data.append([tweetid,tweetdate,polarity])
        #print(polarity)
        #df = pd.DataFrame(x)
        #print(df.head())
        #c.execute("insert into "+targettwitterprofile+" values (?,?,?,?)", (tweetid, tweetdate, tweettext, polarity))
        n+=1
   # time.sleep(65)

dfNew = pd.DataFrame(data, columns=cols)
#print(data)
#df['tweetid'] = tweetid
#df['tweetdate'] = tweetdate
#df['polarity'] =  polarity                                                                                   

#print(df['polarity'])
print(dfNew.head()) 

#print(x)

#conn.commit()
#c.close()
