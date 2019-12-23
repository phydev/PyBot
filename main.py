import tweepy as tw
import numpy as np
import matplotlib.pyplot as plt
from get_code import get_code
from os import environ


# the access keys are defined as environment variables in the server
consumer_key = environ['consumer_key']
consumer_secret = environ['consumer_secret']
access_token = environ['access_token']
access_token_secret = environ['access_token_secret']
number_of_images = environ['number_of_images']

# authenticating
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

user = api.me()

access_list = ['1134771227078402048', '1009108514655096832'] # username ids

phrases_plot = [' Hi there! Your plot is ready. ',
       ' There you go! ',
       ' It\'s my pleasure to help. Here it\'s your graph. ',
       ' Wow! Nice plot! ',
       ' Hmm... I\'m not sure about what we\'re seeing here. ',
       ' PyBot reporting for duty! ']

phrases_error = [' I\'m tired, leave me alone! -.- ',
             ' Compute yourself! ',
             ' I\'m sorry. I can\'t compute that! ',
             ' bip bop bip bop ',
             ' Exterminate! Exterminate! ']

def plt2file(x,y):
    """ 
        function for ploting
        :param x: 1d-array with the x-axis data
        :param y: 1d-array with the y-axis data
        :return:
    """
    plt.plot(x,y)
    plt.savefig('graph.png',dpi=300)
    
    return

def answer_back(message, user_screen_name, phrases_plot, id_):
    if 'run' in message:
        if 'from' in message:
            filename = message.lstrip('@pybotexec run from')
            code = get_code('phydev', 'gists', filename)
            exec(code)                                              
            api.update_status('@' + user_screen_name + ' executed external code with success! ' , id_)
        else:
            exec(message.lstrip('@pybotexec run'))
            api.update_status('@' + user_screen_name + ' executed with success! ' , id_)
    elif 'evaluate' in message:
        expression = message.lstrip('@pybotexec evaluate')
        if '1/0' in expression:
              image = str(np.random.randint(number_of_images)+1)
              api.update_with_media('zeroDivision/zeroDivision'+image+'.jpg','@' + user_screen_name + ' What have you done?! :O #PyBotConsole', id_)
        else:
              code = eval(expression)
              api.update_status('@' + user_screen_name + ' return ' + str(code) +' #PyBotConsole', id_)
    elif 'plot' in message:
        response = np.random.choice(phrases_plot)
        x = np.linspace(0, 100, 200)
        y = eval(message.lstrip('@pybotexec plot'))
        plt2file(x, y)
        api.update_with_media('graph.png', '@' + user_screen_name +' '+  response + ' #PyBotConsole', id_)
    elif 'talk to me!' in message:
        response = ' Hello there, what would you like to talk about? :) '
        api.update_status('@' + user_screen_name +' '+ response + ' #PyBotConsole', id_)      
    return

class MyStreamListener(tw.StreamListener):
    """
        overriding the class streamListener in tweepy with our demands
    """

    def on_status(self, status):
        """
            this function listen to tweets in real time and process it accordingly to the 
            commands submited by the user
            :param status: tweet JSON object
        """
        
        user_screen_name = status.user.screen_name
        user = api.get_user(screen_name=user_screen_name)
        id_ = status.id
        url = 'https://twitter.com/' + user_screen_name + '/status/' + str(id_)
        status_ext = api.get_status(id=id_, tweet_mode='extended')
        message = status_ext.full_text.lower()
        print(message)       
        print("the user.id is in the access list? ", str(user.id) in access_list)
        try:  
            if str(user.id) in access_list:
                answer_back(message, user_screen_name, phrases_plot, id_)
        except:
            response = np.random.choice(phrases_error)
            api.update_status('@' + user_screen_name +' '+ response + ' #PyBotConsole', id_)
            print('Exception!')
            pass


if __name__ == '__main__':
    print('PyBot is starting')
    print('Logged in as ', user.name)
    track = ['@PyBotExec run', '@PyBotExec exec', '@PyBotExec plot'] # following the keywords
    myStreamListener = MyStreamListener() # declaring the listener
    myStream = tw.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended') # starting the streamer
    myStream.filter(track=track, follow=access_list) # listening
    
