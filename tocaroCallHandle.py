#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib
import urllib2
import requests
import json
import re
import datetime
import time
import subprocess


########################################
# Class変数定義
########################################
class TocaroApi(object):
    def __init__(self):
        self.tocaro_id = "tvw7eqgpuktidyekelztqeizhzgwze9z"
        self.base_url = "https://hooks.tocaro.im/integrations/inbound_webhook/"

        self.request_id = 1

########################################
#
########################################
    def sendMessage(self, title, value):

        url = self.base_url + self.tocaro_id

        payload = {"text": "ZBX detected failure",
                   "attachments": [{"title": title, "value": value}]}

        # debug
        debugflag = 1
        if debugflag == 1:
            fd = open('/home/ansible/pythonTools/log/otrs.log', 'a')
            fd.write("tocaro_title= " + title + "\n")
            fd.write("value= " + value + "\n")
            fd.write("url= " + url + "\n")
            fd.close()

        headerstr = {'Content-type': 'application/json',
                     'Accept-Encoding': None}
        # python仕様で呼べず。無念。。
        cmd = "curl -X POST --data-urlencode 'payload=" + json.dumps(payload) \
              + "' " + "'" + url + "'"
        proc = subprocess.call(cmd, shell=True)
