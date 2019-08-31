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

        user_screen_name = status.user.screen_name
        user = api.get_user(screen_name = user_screen_name)
        id = status.id
        url = 'https://twitter.com/' + user_screen_name + '/status/' + str(id)
 

        
        try:
            status_ext = api.get_status(id=id, tweet_mode='extended')
            message = status_ext.full_text.lower()
            print(message)
            print(user.id==1009108514655096832)
            if user.id==1009108514655096832:
                if 'run' in message:
                   code = exec(message.lstrip('@PyBotExec run'))
                elif 'evaluate' in message:
                   code = eval(message.lstrip('@PyBotExec evaluate'))
               
                api.update_status('@'+user_screen_name+'here is your computation: '+ str(code), id)
                print('@'+user_screen_name+'here is your computation: '+ str(code))
                #api.retweet(id)

        except:
            pass
  


    

myStreamListener = MyStreamListener()
myStream = tw.Stream(auth = api.auth, listener=myStreamListener, tweet_mode='extended')

track = ['@PyBotExec ']

myStream.filter(track=track, follow='1009108514655096832')
