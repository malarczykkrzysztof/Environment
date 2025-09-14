import re 
import json
from urllib.parse import urljoin
import requests
USERS_API = "https://api.github.com/users/"

class Twitter(object):
    version = "1.0"
    
    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []
        self.username = username
        
    @property
    def tweets(self):
        if self.backend and not self._tweets:
            backend_text = self.backend.read()
            if backend_text:
                self._tweets = json.loads(backend_text )
        return self._tweets
    
    @property
    def tweet_messages(self):
        return [tweet['message'] for tweet in self.tweets]
    
    def get_user_avatar(self): 
        if not self.username:
            return None 
        url = urljoin(USERS_API, self.username)
        resp = requests.get(url)
        return resp.json()['avatar_url']
    
    
    def tweet (self, message):
        if len(message) > 160:
            raise ValueError("Tweet is too long")
        self.tweets.append({
            'message':message,
            'avatar':self.get_user_avatar(),
            'hashtags': self.find_hashtag(message)
            })
        if self.backend:
            with open (self.backend, 'w') as twitter_file:
                twitter_file.write(json.dumps(self.tweets))
        
    def find_hashtag(self, message): 
        return [m.lower() for m in  re.findall(r"#(\w+)", message)]
    
    def get_all_hashtags(self):
        hashtags = []
        for message in self.tweets:
            hashtags.extend(message['hashtags'])
        if hashtags:
            return set(hashtags)
        return "No hastags found"
        
        