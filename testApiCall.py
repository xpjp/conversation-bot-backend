#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

response = requests.get('http://ec2-52-193-216-160.ap-northeast-1.compute.amazonaws.com:8080/analyze_last_tweet')
# print response.text

decode_json_data = json.loads(response.text)
print decode_json_data[0]['sentence']
