import pytest
import requests
from  my_project import twitter
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

class ResponseGetMock():
    def json(self):
        return {'avatar_url':'test'}

@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param

@pytest.fixture(params=['list','backend'],name = "new_twitter")
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        new_twitter = twitter.Twitter(username=username)
    elif request.param == 'backend':
        new_twitter = twitter.Twitter(backend=backend, username=username) 
    return new_twitter    

def test_initailization(new_twitter):
    assert new_twitter

@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_single(avatar_mock, new_twitter):
    new_twitter.tweet("Hello World")
    assert new_twitter.tweet_messages == ["Hello World"]
    
def test_tweet_lenght(new_twitter):
    with pytest.raises(Exception):
        new_twitter.tweet("tweet" * 50)
    assert new_twitter.tweet_messages == []
    
@pytest.mark.parametrize("message, expected",(
    (" Test #first message", ["first"]),
    ("#First message", ["first"]),
    ("#first message", ["first"]),
    ("first message #rolka", ["rolka"]),
    ("oto moja #first message #rolka", ["first","rolka"])
    ))
def test_twet_with_hashtag(new_twitter, message, expected):
    assert new_twitter.find_hashtag(message) == expected 
    
def test_initialize_two_twitter_class(backend):
    twitter1 = twitter.Twitter(backend=backend)
    twitter2 = twitter.Twitter(backend=backend)
    
    twitter1.tweet("test1")
    twitter2.tweet("test2")
    assert twitter2.tweet_messages == ["test1", "test2"]

@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username(avatar_mock, new_twitter):
    if not new_twitter.username:
        pytest.skip()
    
    new_twitter.tweet("Test message")
    assert new_twitter.tweets == [{"message": "Test message", 
                                   "avatar": "test",
                                   'hashtags':[]}]
    avatar_mock.assert_called()
    
@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hastag_mock(svstsr_mock,new_twitter):
    new_twitter.find_hashtag = Mock() 
    new_twitter.find_hashtag.return_value = ['first']
    new_twitter.tweet("Test #second")
    assert new_twitter.tweets[0]['hashtags'] == ['first']
    new_twitter.find_hashtag.assert_called_with("Test #second")
    
    
def test_twitter_version(new_twitter):
    twitter.version = MagicMock()
    twitter.version.__eq__.return_value = "2.0"
    assert twitter.version == "2.0"
    
@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_hastags(svstsr_mock, new_twitter):
    new_twitter.tweet("Test1 #first")
    new_twitter.tweet("Test1 #first #second")
    new_twitter.tweet("Test1 #third") 
    assert new_twitter.get_all_hashtags() == {"first", "second", "third"}
    
@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_hastags_not_found(svstsr_mock, new_twitter):
    assert new_twitter.get_all_hashtags() == "No hastags found"
    
    
    
    

    

    

    
    
    
    
    