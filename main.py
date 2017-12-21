#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tweepy import *
import sys

from Twapi import *
from Psgr import *
from Analyze import *

def set_default_encoding(charset):
    try:
        #print sys.getdefaultencoding()
        sys.setdefaultencoding(charset)
    except AttributeError:
        reload(sys)
        sys.setdefaultencoding(charset)
        #print sys.getdefaultencoding()

# twt = Twapi()
# api = twt.getAPIInstance()

# try:
#     for value in range(0,15):
#         print api.home_timeline()[value].text
# except TweepError, e:
#     print 'error'

# psgr = Psgr()
# cur = psgr.getCur()
#
# cur.execute("select * from users")
# for row in cur:
#     print(row)
#
# psgr.dbCommit()

def main():
    # utf-8に変更
    set_default_encoding('utf-8')
    # PsgrのInstance作成

    # ツイートの取得
    # twt = Twapi()
    # api = twt.twitter_api
    # status = api.home_timeline()[0]
    #
    # sentence = status.text
    # tweet_id = status.id
    # user_id = status.user.screen_name
    # user_name = status.user.name
    sentence  = "すもももももももものうち"
    tweet_id  = 760430632317038592
    user_id   = "snow_moment09"
    user_name = "雪村刹那"

    # データベースInstanceの作成
    psgr = Psgr()
    try:
        #トランザクション処理開始
        psgr.begin()
        values = (sentence,tweet_id,user_id,user_name)
        sqlcom = "INSERT INTO sentences (sentence,tweet_id,user_id,user_name) VALUES (%s,%s,%s,%s) RETURNING sentence_id;"
        psgr.execute(sqlcom,values)
        sentence_id = psgr.lastrowid()

        # テキストの解析
        analyze = Analyze()
        # print analyze.get_version()
        parse_data = analyze.parse_sentence(sentence.encode('utf-8'))
        for data in parse_data:
            # print data[0],'\t',data[1].split(',')[0]
            detail_array = ['*'] * 9
            detail_array[:len(data[1].split(','))] = data[1].split(',')

            # 登録用データ↓↓
            word = data[0]
            part_of_speech = detail_array[0]
            if part_of_speech == "BOS/EOS":
                continue

            part_of_speech_detail1 = detail_array[1]
            part_of_speech_detail2 = detail_array[2]
            part_of_speech_detail3 = detail_array[3]
            conjugate1 = detail_array[4]
            conjugate2 = detail_array[5]
            original = detail_array[6]
            pronunciation1 = detail_array[7]
            pronunciation2 = detail_array[8]

            values = (word,part_of_speech,part_of_speech_detail1,part_of_speech_detail2,part_of_speech_detail3,conjugate1,conjugate2,original,pronunciation1,pronunciation2)
            sqlcom = "INSERT INTO words (word,part_of_speech,part_of_speech_detail1,part_of_speech_detail2,part_of_speech_detail3,conjugate1,conjugate2,original,pronunciation1,pronunciation2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING word_id;"
            psgr.execute(sqlcom,values)
            word_id = psgr.lastrowid()

            values = (sentence_id,word_id)
            sqlcom = "INSERT INTO sentence_word (sentence_id,word_id) VALUES (%s,%s) RETURNING sentence_word_id;"
            psgr.execute(sqlcom,values)

        psgr.commit()
        del analyze
    except Exception as e:
        print e
        psgr.rollback()




    del psgr
    # del twt

if __name__ == "__main__":
    main()

#    psgr = Psgr()
#    print "\n"
#    psgr.showTable('sentences')
#    print "\n"
#    psgr.showTable('words')
#    print "\n"
#    psgr.showTable('sentence_word')



    # analyze = Analyze()
    # print analyze.get_version()
    # parse_data = analyze.parse_sentence("太郎はこの本を二郎を見た女性に渡した。")
    # for data in parse_data:
    #     print data[0],'\t',data[1]
