import sys,os
sys.path.append('/home/xpjp/analyze_api')
from Psgr import *
from Analyze import *

import simplejson as json
from bottle import route, request, run, template, HTTPResponse

@route('/hello')
def index(name):
    return "hello world"

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
    print("[markov_chain]")
    cur.execute("select * from markov_chain")
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
    cur.execute("DELETE FROM markov_chain")

    psgr.dbCommit()
    del psgr

    # responseを作成
    return make_response('deleted')


@route('/insert', method='POST')
def insert():
    # psgr = Psgr()
    # cur = psgr.getCur()

    # 送られてきたJSONを読み込む
    postdata = request.body.read()
    print (postdata)
    json_dict = json.loads(postdata)
    print(type(json_dict), json_dict['sentence'])

    sentence = json_dict['sentence']
    channel_id = str(json_dict['channel_id'])
    channel = json_dict['channel']

    # messageを登録
    sentence_id = insert_message(sentence,channel_id)
    # messageを解析(機械学習用に溜めとくため)
    analyze_message(sentence,sentence_id,channel_id)
    # チャンネル情報を登録
    insert_channels(channel_id, channel)
    # markov連鎖用データ登録
    insert_data_markov(sentence_id,sentence, channel_id)

    return make_response("登録されました")

# markov連鎖で文章作成
@route('/talk', method='GET')
def talk():
    return make_response(make_sentence(390124129430536194))

# messageの解析
def analyze_message(sentence, sentence_id,channel_id):
    psgr = Psgr()
    cur = psgr.getCur()

    # messageの解析
    try:
        psgr.begin()

        analyze = Analyze()
        parse_data = analyze.parse_sentence(sentence)
        for data in parse_data:
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
            values = (word,part_of_speech,part_of_speech_detail1,part_of_speech_detail2,part_of_speech_detail3,conjugate1,conjugate2,original,pronunciation1,pronunciation2)
            sqlcom = "INSERT INTO words (word,part_of_speech,part_of_speech_detail1,part_of_speech_detail2,part_of_speech_detail3,conjugate1,conjugate2,original,pronunciation1,pronunciation2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING word_id;"
            psgr.execute(sqlcom,values)
            word_id = psgr.lastrowid()

            # 単語と文章を繋ぐ
            values = (sentence_id,word_id,channel_id)
            sqlcom = "INSERT INTO sentence_word (sentence_id, word_id, channel_id) VALUES (%s,%s,%s) RETURNING sentence_word_id;"
            psgr.execute(sqlcom,values)

    except Exception as err:
        print(err)
        psgr.rollback()

    # コミット
    psgr.dbCommit()
    del psgr

def insert_message(sentence, channel_id):
    psgr = Psgr()
    cur = psgr.getCur()

    # messageを登録
    sentence_id = -1
    try:
        psgr.begin()
        values = (sentence, channel_id)
        sqlcom = "INSERT INTO sentences (sentence, channel_id) VALUES (%s,%s) RETURNING sentence_id;"
        psgr.execute(sqlcom,values)
        sentence_id = psgr.lastrowid()

    except Exception as err:
        print(err)
        psgr.rollback()

    # コミット
    psgr.dbCommit()
    del psgr

    return sentence_id

def insert_channels(channel_id, channel):
    psgr = Psgr()
    cur = psgr.getCur()

    # チャンネル情報を登録
    try:
        psgr.begin()
        cur.execute("select * from channels")
        data = cur.fetchall()

        exist_id = False
        for row in data:
            if int(row[2]) == int(channel_id):
                exist_id = True
                break

        if not exist_id:
            print("insert channel")
            values = (channel_id, channel)
            sqlcom = "INSERT INTO channels (channel_id, channel) VALUES (%s,%s)"
            psgr.execute(sqlcom,values)

    except Exception as err:
        print(err)
        psgr.rollback()

    # コミット
    psgr.dbCommit()
    del psgr

# 文章を分かち書きしてDBに登録する
def insert_data_markov(sentence_id,sentence, channel_id):
    # データベースInstanceの作成
    psgr = Psgr()
    try:
        #トランザクション処理開始
        psgr.begin()

        # messageの形態素解析
        analyze = Analyze()
        # 分かち書きした文章を取得する
        # 吾輩 は 猫 で ある
        parse_data = analyze.parse_wakati_sentence(sentence)

        w1 = ''
        w2 = ''
        for data in parse_data:
            if data[0] == '':
                continue
            # 登録用データ↓↓
            word = data[0]
            if w1 and w2:
                values = (sentence_id, w1, w2, word, channel_id)
                sqlcom = "INSERT INTO markov_chain (sentence_id, word1, word2, word3, channel_id) VALUES (%s,%s,%s,%s,%s)"
                psgr.execute(sqlcom,values)
            w1, w2 = w2, word

        psgr.commit()
        del analyze
    except Exception as e:
        print (e)
        psgr.rollback()

    del psgr

# 文章作成
def make_sentence(channel_id):
    # データベースInstanceの作成
    sentence = ""
    psgr = Psgr()
    try:
        #トランザクション処理開始
        psgr.begin()
        cur = psgr.getCur()
        # 1単語目所得
        cur.execute("SELECT * FROM markov_chain WHERE word1 = 'これ' AND channel_id = "+ str(channel_id) +" ORDER BY random() LIMIT 1")
        list1 = cur.fetchall()
        w1 = list1[0][2]
        w2 = list1[0][3]
        sentence += w1 + w2

        word_count = 0
        loop_count = 3 # 最初の2単語+終了単語
        while True:
            if w1 == w2:
                bRet = False
                print ("失敗:w1 = w2" + sentence)
                break
            loop_count += 1
            obj_len = -1
            obj = None

            sqlcom = "SELECT * FROM markov_chain WHERE word1 = '" + w1 + "' AND word2 = '" + w2 + "' ORDER BY random() LIMIT 1"
            psgr.execute(sqlcom,[])
            obj = psgr.fetchall()
            obj_len = len(obj)
            if not (obj_len > 0):
                bRet = False
                print ("失敗:not object" + sentence)
                break

            w3 = obj[0][4]

            # if loop_count > 100:
            #     bRet = False
            #     print ("失敗:loop over" + sentence)
            #     break
            # elif word_count > 100:
            #     bRet = False
            #     print ("失敗:word over" + sentence)
            #     break

            w1, w2 = w2, w3
            sentence += w3
            word_count += 1

        psgr.commit()
    except Exception as e:
        print (e)
        psgr.rollback()
    finally:
        del psgr

    return sentence

# 返却message作成
def make_response(message):
    body = json.dumps({'message': message})
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json;charset=utf-8')
    return response

if __name__ == '__main__':

    # run(host='localhost', port=8080)
    run(host='198.13.43.77', port=8080)

else:
    run(host='198.13.43.77', port=8080)
