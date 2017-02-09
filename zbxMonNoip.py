#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import boto3
import json
import shutil
import os
import subprocess
import time

import zbxHostIFset as zbxIpCtr

## parameter define
instanceListNm = "/home/ansible/pythonTools/data/instanceList.txt"
tmpInitlist = "/home/ansible/pythonTools/data/tmpInitlist"

inifhn = open(tmpInitlist,"r")
tmpInitList = inifhn.readlines()
inifhn.close()

fhn = open(instanceListNm,"r")
allInstanceList = fhn.readlines()
fhn.close()

if tmpInitList != "":
  # IPアドレスからをzbxホスト名を取得
  for ipaddr1 in tmpInitList:
    ipaddr = ipaddr1.replace('\n','')
    for thisline1 in allInstanceList:
      thisline = thisline1.replace('\n','')

      if thisline.find(ipaddr) >= 0:
        tmpthis = thisline.split(',')[1]
        hostnm = tmpthis.split('.')[0]

        time.sleep(20)
        zbxIpCtr.setIpAddr(hostnm)
  # tmpInitlistを空白に
  inifhn = open(tmpInitlist,"w")
  inifhn.write("")
  inifhn.close()
