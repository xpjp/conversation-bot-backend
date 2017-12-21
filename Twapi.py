#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import codecs
import tweepy

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class Twapi(object):
    """docstring for Twapi"""
    def __init__(self):
        super(Twapi, self).__init__()
        # 各種キーをセット
        self.__CONSUMER_KEY    = 'bKhEIbP6YUCgY8jIqGapmnGzf'
        self.__CONSUMER_SECRET = 'i6AvnQq8rOEF1JwUAEe5D3OLgaBKBUycNDpZUmUbS3QxSnnpei'
        auth = tweepy.OAuthHandler(self.__CONSUMER_KEY, self.__CONSUMER_SECRET)
        self.__ACCESS_TOKEN  = '3470506034-RHTIDE5lG49qum31dZdMzqJX6N3fvWCO5y27NNt'
        self.__ACCESS_SECRET = 'irPNHaNGouXUzoOsSUDT9KatlmuuGj6f89FBbmSPHVYoF'
        auth.set_access_token(self.__ACCESS_TOKEN, self.__ACCESS_SECRET)
        # これだけで、Twitter APIをPythonから操作するための準備は完了。
        #APIインスタンスを作成
        self.twitter_api = tweepy.API(auth)
        print "***Hello Twapi!***"

    # デストラクタ
    def __del__(self):
        print "***Bye Twapi!***"


# twt = Twapi()
# api = twt.getAPIInstance()
#
# status_to_tweet = "testTweetab"
# api.update_status(status_to_tweet)
# print('Done!')

# print api.home_timeline()[0]
# print('Done!')

# search_result = api.search(q='初音ミク')
# for result in search_result:
#     print result.text
