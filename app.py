import sys,os
sys.path.append('/home/xpjp/analyze_api')
from Psgr import *

import simplejson as json
from bottle import route, request, run, template, HTTPResponse

@route('/hello')
def index(name):
    return "テスト" + " abc"

@route('/all/delete',method='GET')
def delete():
    psgr = Psgr()
    cur = psgr.getCur()

    cur.execute("DELETE FROM CHANNELS")

    psgr.dbCommit()
    del psgr

    body = json.dumps({'message': 'deleted'})
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json')
    return response

@route('/insert', method='POST')
def insert():
    psgr = Psgr()
    cur = psgr.getCur()

    postdata = request.body.read()
    print (postdata)
    json_dict = json.loads(postdata)
    print(type(json_dict), json_dict['sentence'])

    cur.execute("insert into sentences (sentence, channelid) values('test:" + json_dict['sentence'] + "', " + str(json_dict['channelid']) + ")")

    cur.execute("select * from channels")
    data = cur.fetchall()

    exist_id = False
    for row in data:
        if row[2] == json_dict['channelid']:
            exist_id = True
            break

    if not exist_id:
        cur.execute("insert into channels (channelid, channel) values(" + str(json_dict['channelid']) + ", '" + json_dict['channel'] + "')")

    psgr.dbCommit()

    del psgr

    body = json.dumps({'message': '登録されました。'})
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json')
    return response

@route('/all/select',method='GET')
def select():
    psgr = Psgr()
    cur = psgr.getCur()

    cur.execute("select * from sentences")
    for row in cur:
        print(row)

    print("---------------")

    cur.execute("select * from channels")
    for row in cur:
        print(row)

    # psgr.dbCommit()
    del psgr

    body = json.dumps({'message': 'selected'})
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json')
    return response

if __name__ == '__main__':

    # run(host='localhost', port=8080)
    run(host='198.13.43.77', port=8080)

else:
    application = default_app()
