import tweepy as tw
import numpy as np
import matplotlib.pyplot as plt
from os import environ


# the access keys are defined as environment variables in the server
consumer_key = environ['consumer_key']
consumer_secret = environ['consumer_secret']
access_token = environ['access_token']
access_token_secret = environ['access_token_secret']

# authenticating
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

user = api.me()
print("Logged in as ", user.name)


def plt2file(x, y):
    plt.plot(x, y)
    plt.savefig('graph.png', dpi=300)
    return


class MyStreamListener(tw.StreamListener):

    def on_status(self, status):

         user_screen_name = status.user.screen_name
         user = api.get_user(screen_name=user_screen_name)
         id_ = status.id
         url = 'https://twitter.com/' + user_screen_name + '/status/' + str(id_)
         print(url)
         try:
             status_ext = api.get_status(id=id_, tweet_mode='extended')
             message = status_ext.full_text.lower()
             print(message)
             print(str(user.id) in access_list)
             if str(user.id) in access_list:
                 if 'run' in message:
                     code = exec(message.lstrip('@pybotexec run'))
                     print(code)
                     print('@' + user_screen_name + ' return ' + str(code))
                     api.update_status('@' + user_screen_name + ' return ' + str(code), id_)
                     print('@' + user_screen_name + ' return ' + str(code))
                 elif 'evaluate' in message:
                     code = eval(message.lstrip('@pybotexec evaluate'))
                     print(code)
                     print('@' + user_screen_name + ' return ' + str(code))
                     api.update_status('@' + user_screen_name + ' return ' + str(code), id_)
                     print('@' + user_screen_name + ' return ' + str(code))
                 elif 'plot' in message:
                     response = 'merda' #np.random.choice(phrases_plot)
                     x = np.linspace(0, 100, 200)
                     y = eval(message.lstrip('@pybotexec plot'))
                     plt2file(x, y)
                     api.update_with_media('graph.png', '@' + user_screen_name + response, id_)
                 elif 'talk' in message:
                     response = ' Hello there, what would you like to talk about? :)'
                     api.update_status('@' + user_screen_name + response, id_)
                 # api.retweet(id)
         except:
             print('mai que caralha!')
             response = 'merda!'#np.random.choice(phrases_error)
             api.update_status('@' + user_screen_name + response, id_)
             print('Exception!')

phrases_plot = [' Hi there! Your plot is ready:',
           ' There you go:',
           ' It\'s my pleasure to help. Here it\'s your graph ',
           ' Wow! Nice plot!',
           ' Hmm... I\'m not sure about what we\'re seeing here. ',
           ' PyBot reporting for duty! ']

phrases_error = [' I\'m tired, leave me alone! -.-',
                 ' Compute yourself!',
                 ' I\'m sorry. I can\'t compute that!',
                 ' bip bop bip bop',
                 ' Exterminate! Exterminate! ']

access_list = ['1009108514655096832', '1134771227078402048']
myStreamListener = MyStreamListener()
myStream = tw.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended')
#api.send_direct_message(recipient_id=1009108514655096832, text='response')
track = ['@PyBotExec ']

myStream.filter(track=track, follow=access_list)
