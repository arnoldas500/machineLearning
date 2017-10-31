from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#import MySQLdb
import time
import json



#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL usernameMySQL pass  Database name.
#conn = MySQLdb.connect("mysql.server","beginneraccount","cookies","beginneraccount$tutorial")

#c = conn.cursor()


#consumer key, consumer secret, access token, access secret.
consumer_key = 'E3xLP2DJVCojAuRc4dsIQhOhH'
consumer_secret = '46e1t5l5uZDUY3WfuNf0NwzsNVdPnJS7qtVjVc6HKwxfH0BYX4'

access_token = '398425873-SL80lXVpCqZN8zTTNWSz6pBWRdy1CwzdWQlRrBEu'
access_token_secret = 'FAmHxrdwJfnrcjRVKvuxVRpoQfezjS7npTc6dH20EfwAq'

class listener(StreamListener):

    def on_data(self, data):
        try:
            print(data)
        #saving to a file
            savef = open('twitDB.csv','a')
            savef.write(data)
        #add new line
            savef.write('\n')
            savef.close()
        except BaseException, e:
            print("failed ondata,",str(e))
            time.sleep(5)

        #saving to a database
        '''
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]
        
        c.execute("INSERT INTO taula (time, username, tweet) VALUES (%s,%s,%s)",
            (time.time(), username, tweet))

        conn.commit()

        print((username,tweet))
        '''
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["bitcoin"])
