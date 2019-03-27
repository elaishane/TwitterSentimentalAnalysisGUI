from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob
import matplotlib.pyplot as plt
 
import tweepy_credentials

import numpy as np
import pandas as pd
import re


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
    	auth = OAuthHandler(tweepy_credentials.CONSUMER_KEY, tweepy_credentials.CONSUMER_SECRET)
    	auth.set_access_token(tweepy_credentials.ACCESS_TOKEN, tweepy_credentials.ACCESS_TOKEN_SECRET)
    	self.auth = auth
    	self.twitter_client = API(self.auth)

    	self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    
'''
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)
'''
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        pos1 = 0
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweets'])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df