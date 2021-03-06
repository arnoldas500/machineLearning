import os
import sys
import tweepy
import requests
import numpy as np
import textblob

#from keras.models import Sequential
#from keras.layers import Dense
#from textblob import TextBlob

consumer_key = 'E3xLP2DJVCojAuRc4dsIQhOhH'
consumer_secret = '46e1t5l5uZDUY3WfuNf0NwzsNVdPnJS7qtVjVc6HKwxfH0BYX4'

access_token = '398425873-SL80lXVpCqZN8zTTNWSz6pBWRdy1CwzdWQlRrBEu'
access_token_secret = 'FAmHxrdwJfnrcjRVKvuxVRpoQfezjS7npTc6dH20EfwAq'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#now since we have the api variable we can create tweets delete tweets and find twitter users                                                                                        
userApi = tweepy.API(auth)

def get_sentiment(polarity):
    if polarity < 0:
        return "negative"
    elif polarity == 0:
        return "neutral"
    else:
        return "positive"

def stock_sentiment(quote, num_tweets):
    # Checks if the sentiment for our quote is
    # positive or negative, returns True if
    # majority of valid tweets have positive sentiment
    list_of_tweets = userApi.search(quote, count=num_tweets)
    positive, objective, neg, sub, neut  = 0, 0, 0, 0, 0 

    for tweet in list_of_tweets:
        blob = textblob.TextBlob(tweet.text).sentiment
#The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
        if blob.subjectivity == 0:
            objective += 1
            #next
        if blob.polarity > 0:
            positive += 1
        if blob.polarity < 0:
            neg += 1
        if blob.subjectivity == 1:
            sub +=1
        if blob.polarity == 0:
            neut +=1

    score = positive / ((num_tweets - objective)/2)
    print("how its doing ",score)
    print("values pos", positive, "negative values ", neg, "neutral", neut)
    print("how many objective tweets ",objective, "num of subjective tweets", sub)
    print("total tweets analyzed was ", num_tweets)
    if positive > ((num_tweets - objective)/2):
        return print("true")


stock_sentiment('ethereum', 100000)
