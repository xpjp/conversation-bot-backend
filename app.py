import sys,os
sys.path.append('/home/xpjp/analyze_api')
from Psgr import *

import simplejson as json
from bottle import route, request, run, template, HTTPResponse

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/insert',method='POST')
def insert():
    psgr = Psgr()
    cur = psgr.getCur()

    postdata = request.body.read()
    print (postdata)
    json_dict = json.loads(postdata)
    print(type(json_dict), json_dict['sentence'])

    cur.execute("insert into sentences (sentence) values('test:" + json_dict['sentence'] + "')")
    psgr.dbCommit()
    
    del psgr

    body = json.dumps({'message': '登録されました。'})
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json')
    return response

@route('/select',method='GET')
def select():
    psgr = Psgr()
    cur = psgr.getCur()

    cur.execute("select * from sentences")
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
