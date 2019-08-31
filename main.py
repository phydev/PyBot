import tweepy as tw
from os import environ
import time

consumer_key = environ['consumer_key']
consumer_secret = environ['consumer_secret']
access_token = environ['access_token']
access_token_secret = environ['access_token_secret']

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)



class MyStreamListener(tw.StreamListener):
 

    def on_status(self, status):

        user = status.user.screen_name
        id = status.id
        url = 'https://twitter.com/' + user + '/status/' + str(id)
 

        wall = False
        try:
            status_ext = api.get_status(id=id, tweet_mode='extended')
            message = status_ext.full_text.lower()
            print(message)

            if status.user.id==1009108514655096832:
                code = eval(message.lstrip('@PyBotExec >>'))
                api.update_status('@'+user+'here is your computation: '+code, id)
                print('@'+user+'here is your computation: '+code)
                #api.retweet(id)

        except:
            pass
  


    

myStreamListener = MyStreamListener()
myStream = tw.Stream(auth = api.auth, listener=myStreamListener, tweet_mode='extended')

track = ['@PyBotExec']

myStream.filter(track=track, follow='1009108514655096832')
