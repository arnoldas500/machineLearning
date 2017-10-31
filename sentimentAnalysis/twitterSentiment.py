#using natural language processing on twitter to see how people feel about a specific topic
#sentiment alaysis works by breaking down a text by tokenization 
#becaues we are creating small tokens of large text
#break down each word into its own token and count how many times it was used
#using twitters API

import tweepy
import textblob

consumer_key = 'E3xLP2DJVCojAuRc4dsIQhOhH'
consumer_secret = '46e1t5l5uZDUY3WfuNf0NwzsNVdPnJS7qtVjVc6HKwxfH0BYX4'

access_token = '398425873-SL80lXVpCqZN8zTTNWSz6pBWRdy1CwzdWQlRrBEu'
access_token_secret = 'FAmHxrdwJfnrcjRVKvuxVRpoQfezjS7npTc6dH20EfwAq'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#now since we have the api variable we can create tweets delete tweets and find twitter users
api = tweepy.API(auth)

#searching for tweets tht have trump in it
public_tweets = api.search('bitcoin')

#loop thru all tweets and analyze using text blob 
#Polarity shows how popular it is (how negative or positive it is)
#can see each tweet and its sentiment alaysis
#subjectivity shows how much of an opinion it is compared to how much of a fact it is
for tweet in public_tweets:
    print(tweet.text)
    analysis = textblob.TextBlob(tweet.text)
    print(analysis.sentiment)

