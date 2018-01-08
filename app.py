import sys,os
sys.path.append('/home/xpjp/analyze_api')
from Psgr import *
from Analyze import *

import simplejson as json
from bottle import route, request, run, template, HTTPResponse

@route('/hello')
def index(name):
    return "テスト" + " abc"

@route('/all/select',method='GET')
def select():
    psgr = Psgr()
    cur = psgr.getCur()

    # データを閲覧する
    print("---------------")
    print("[sentences]")
    cur.execute("select * from sentences")
    for row in cur:
        print(row)

    print("---------------")
    print("[words]")
    cur.execute("select * from words")
    for row in cur:
        print(row)

    print("---------------")
    print("[channels]")
    cur.execute("select * from channels")
    for row in cur:
        print(row)

    print("---------------")
    del psgr

    # responseを作成
    return make_response('selected')

@route('/all/delete',method='GET')
def delete():
    psgr = Psgr()
    cur = psgr.getCur()

    # データを削除する
    cur.execute("DELETE FROM SENTENCES")
    cur.execute("DELETE FROM WORDS")
    cur.execute("DELETE FROM CHANNELS")

    psgr.dbCommit()
    del psgr

    # responseを作成
    return make_response('deleted')


@route('/insert', method='POST')
def insert():
    psgr = Psgr()
    cur = psgr.getCur()

    # 送られてきたJSONを読み込む
    postdata = request.body.read()
    print (postdata)
    json_dict = json.loads(postdata)
    print(type(json_dict), json_dict['sentence'])
    sentence = json_dict['sentence']
    channelid = str(json_dict['channelid'])
    channel = json_dict['channel']

    # messageを形態素解析かけて、データベースに登録する。
    try:
        psgr.begin()
        # messageを登録

        values = (sentence,channelid)
        sqlcom = "INSERT INTO sentences (sentence, channelid) VALUES (%s,%s) RETURNING sentence_id;"
        psgr.execute(sqlcom,values)
        sentence_id = psgr.lastrowid()


        print ("start analyze")
        # テキストの解析
        analyze = Analyze()
        # print analyze.get_version()
        # parse_data = analyze.parse_sentence(sentence.encode('utf-8'))
        parse_data = analyze.parse_sentence(sentence)
        for data in parse_data:
            # print data[0],'\t',data[1].split(',')[0]
            detail_array = ['*'] * 9
            detail_array[:len(data[1].split(','))] = data[1].split(',')

            # 登録用データ↓↓
            # word = data[0] # Surfaceデータが取れないので。
            word = detail_array[6]
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

            # 単語の登録
            print ("insert word")
            values = (word,part_of_speech,part_of_speech_detail1,part_of_speech_detail2,part_of_speech_detail3,conjugate1,conjugate2,original,pronunciation1,pronunciation2)
            sqlcom = "INSERT INTO words (word,part_of_speech,part_of_speech_detail1,part_of_speech_detail2,part_of_speech_detail3,conjugate1,conjugate2,original,pronunciation1,pronunciation2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING word_id;"
            psgr.execute(sqlcom,values)
            word_id = psgr.lastrowid()

            # 単語と文章を繋ぐ
            print ("insert sentence_word")
            values = (sentence_id,word_id,str(json_dict['channelid']))
            sqlcom = "INSERT INTO sentence_word (sentence_id, word_id, channelid) VALUES (%s,%s,%s) RETURNING sentence_word_id;"
            psgr.execute(sqlcom,values)

        print ("commit")
        psgr.commit()
        del analyze

    except Exception as err:
        print(err)
        psgr.rollback()

    # # チャンネル情報を登録
    insert_channels(channelid, channel)
    # cur.execute("select * from channels")
    # data = cur.fetchall()
    #
    # exist_id = False
    # for row in data:
    #     if row[2] == channelid:
    #         exist_id = True
    #         break
    #
    # if not exist_id:
    #     values = (channelid, channel)
    #     sqlcom = "INSERT INTO channels (channelid, channel) VALUES (%s,%s)"
    #     psgr.execute(sqlcom,values)

    # コミット
    psgr.dbCommit()

    del psgr

    # responseを作成
    return make_response("登録されました")

def insert_channels(channelid, channel):
    psgr = Psgr()
    cur = psgr.getCur()

    # チャンネル情報を登録
    try:
        psgr.begin()
        cur.execute("select * from channels")
        data = cur.fetchall()

        exist_id = False
        for row in data:
            if row[2] == channelid:
                exist_id = True
                break

        if not exist_id:
            values = (channelid, channel)
            sqlcom = "INSERT INTO channels (channelid, channel) VALUES (%s,%s)"
            psgr.execute(sqlcom,values)

    except Exception as err:
        print(err)
        psgr.rollback()

    # コミット
    psgr.dbCommit()
    del psgr


def make_response(message):
    body = json.dumps({'message': message})
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json')
    return response

if __name__ == '__main__':

    # run(host='localhost', port=8080)
    run(host='198.13.43.77', port=8080)

else:
    application = default_app()
