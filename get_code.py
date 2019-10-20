import base64
import requests

def get_code(username, repository,filename):
    """
    get a code from a github repository.
    
    :param username: github username
    :param repository: github repository
    :param filename: filename and extension
    :return content: returns the code 
    """

    url = 'https://api.github.com/repos/'+username+'/'+repository+'/contents/'+filename
    print(url)
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
       req = req.json()  # the response is a JSON
       content = base64.decodebytes(bytes(req['content'], 'utf-8' ))
       return content
    else:
       print('Content was not found.')
 
