import tweepy
import csv
import pandas as pd

consumer_key = 'E3xLP2DJVCojAuRc4dsIQhOhH'
consumer_secret = '46e1t5l5uZDUY3WfuNf0NwzsNVdPnJS7qtVjVc6HKwxfH0BYX4'

access_token = '398425873-SL80lXVpCqZN8zTTNWSz6pBWRdy1CwzdWQlRrBEu'
access_token_secret = 'FAmHxrdwJfnrcjRVKvuxVRpoQfezjS7npTc6dH20EfwAq'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#Step 1: Crawl Tweets Against Hash Tags
#####bitcoin
# Open/Create a file to append data
csvFile = open('bitcoinCrawler.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q="#bitcoin",count=1000,
                           lang="en",
                           since="2017-01-01").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

'''
This Twitter Crawler allows you to scrape tweets against hash tags and store the tweets into a csv. scraped all the tweets containing #bitcoin from jan 01, 2017 to April 16, 2017.
'''

#Step 2. Analyzing Tweets for Sentiment

'''
Need to do:
text data is needs to be  preprocessed and stop words need to be filtered out before applying the support vector machine algorithm.

create a text classifier to label each tweet as positive, negative or neutral sentiment

'''


#deal with the Naive Bayes Classifier and Support Vector Machines
