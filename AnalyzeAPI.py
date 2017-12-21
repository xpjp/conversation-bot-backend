#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

from bottle import route, run
from Psgr import *

def set_default_encoding(charset):
    try:
        sys.setdefaultencoding(charset)
    except AttributeError:
        reload(sys)
        sys.setdefaultencoding(charset)

set_default_encoding('utf-8')

# routeデコレーター
# これを使用してURLのPathと関数をマッピングする。
@route('/hello')
def hello():
  return "Hello World!"

@route('/analyze_last_tweet')
def analyze_last_tweet():
    output_data = None
    psgr = Psgr()

    # values = (sentence,tweet_id,user_id,user_name)
    # sqlcom = "INSERT INTO sentences (sentence,tweet_id,user_id,user_name) VALUES (%s,%s,%s,%s) RETURNING sentence_id;"
    output_data = psgr.getParseData((1,))
    print output_data
    del psgr

    jsonstring = json.dumps(output_data)

    return jsonstring

# ビルトインの開発用サーバーの起動
# ここでは、debugとreloaderを有効にしている
run(host='localhost', port=8080, debug=True, reloader=True)
