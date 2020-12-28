#!/usr/bin/env python3
# Analyize the sentiment of the accounts that you follow on Twitter

# Built on the Twitter v2 API

import json
import os
import sys

import requests
from textblob import TextBlob


class Twitter:
    def __init__(self, username):
        self.oauth_endpoint = 'https://api.twitter.com/oauth2/token'
        self.bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
        self.api_url = 'https://api.twitter.com/'
        self.headers = {'Authorization': 'Bearer ' + self.bearer_token}
        self.username = username

    def api_endpoint(self, endpoint: str) -> str:
        '''
        Construct an API endpoint
        '''
        return self.api_url + endpoint

    def get_userid(self, username: str) -> str:
        '''
        Given a twitter username, return the user ID for that username
        '''
        url = self.api_endpoint(f'2/users/by/username/{username}')
        response = requests.get(url, headers=self.headers)
        j = json.loads(response.text)
        return j['data']['id']

    def get_following(self, userid: str) -> str:
        '''
        Get the list of follows for the given user ID
        '''
        url = self.api_endpoint(f'2/users/{userid}/following')
        params = {
            'max_results': 1000
        }
        response = requests.get(url, headers=self.headers, params=params)
        j = json.loads(response.text)
        return j['data']

    def get_tweet_history_for_user(self, userid: str) -> dict:
        '''
        Given a user ID, get their tweets
        Ref https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
        This can return up to 3,200 tweets per user, but is limited to 100 tweets per request
        '''
        url = self.api_endpoint(f'2/users/{userid}/tweets')
        params = {
            'max_results': 100
        }
        response = requests.get(url, headers=self.headers, params=params)
        j = json.loads(response.text)
        if 'data' not in j:
            return []
        return j['data']

    def run(self):
        uid = self.get_userid(self.username)
        print(f'User ID: {uid}')
        follows = self.get_following(uid)
        print(f'This user is following {len(follows)} accounts.')
        for follow in follows:  # For each followed account ... 
            print(f'@{follow["username"]}: {follow["name"]} (User ID: {follow["id"]})')
            tweet_history = self.get_tweet_history_for_user(follow['id'])
            polarity = float(0)
            subjectivity = float(0)
            for tweet in tweet_history:  # Do sentiment analysis for each tweet
                p, s = TextBlob(tweet['text']).sentiment
                polarity = polarity + p
                subjectivity = subjectivity + s
            num_tweets = len(tweet_history)
            polarity_score = polarity / num_tweets
            subjectivity_score = subjectivity / num_tweets
            print(f'  Sentiment score: {round(polarity_score * 100)}% positive, {round(subjectivity_score * 100)}% subjective over the last {len(tweet_history)} tweets.')

if __name__ == "__main__":
    username = sys.argv[1]
    t = Twitter(username)
    if t.bearer_token is None:
        sys.exit("Bearer token not set.")
    t.run()
