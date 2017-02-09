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

########################################
#### Class変数定義
########################################
class OTRSApi(object):
  def __init__(self):
    self.otrs_ip = "172.31.29.38"
    self.otrs_user = "otrs"
    self.otrs_pass = "password"
    self.base_url = "http://" + self.otrs_ip + "/otrs/nph-genericinterface.pl/Webservice/APITicket/"

    self.request_id = 1
########################################
#### チケット作成
########################################
  def CreateTicket(self, title, type, queue, state, priority, customer_user, subject, body):

    url = self.base_url + "Create?"

    ### debug
    debugflag = 1
    if debugflag == 1:
      fd = open('/home/ansible/pythonTools/log/otrs.log', 'a')
      fd.write("**************************\n")
      fd.write("title= "+ title + "\n")
      fd.write("type= "+ type + "\n")
      fd.write("queue= "+ queue + "\n")
      fd.write("state= "+ state + "\n")
      fd.write("priority= "+ priority + "\n")
      fd.write("customer_user= "+ customer_user + "\n")
      fd.write("subject= "+ subject + "\n")
      fd.write("body= "+ body + "\n")
      fd.close()

    payload = {"UserLogin": self.otrs_user,
               "Password": self.otrs_pass,
               "Ticket":
                 {"Title": title,
                  "Type": type,
                  "Queue": queue,
                  "State": state,
                  "Priority": priority,
                  "CustomerUser": customer_user},
                "Article":
                  {"Subject": subject,
                   "Body": body,
                   "ContentType": "text/plain; charset=utf8"
                  }
               }

    headerstr = {'Content-type': 'application/json', 'Accept-Encoding': None}
    response = requests.post(url, data=json.dumps(payload), headers=headerstr)

    rtnstr = response.json()
    newid = rtnstr['TicketID']
##    print newid

    return newid

########################################
#### チケット一覧取得
########################################
  def Search(self, methodType):
    url = self.base_url + "Search?"

    params = urllib.urlencode(
              {'UserLogin': self.otrs_user,
               'Password': self.otrs_pass,
              })

    # GET
    response = urllib.urlopen(url + params)
##    print response.code
    return response.read()

