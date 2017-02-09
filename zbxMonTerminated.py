#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import boto3
import json
import shutil
import os
import subprocess
import time

## parameter define
instanceListNm = "/home/ansible/pythonTools/data/instanceList.txt"
insToHostNm = "/home/ansible/pythonTools/data/insToHostnmList.txt"

fhn = open(instanceListNm,"r")
allInstanceList = fhn.readlines()
fhn.close()

ith_fhn = open(insToHostNm,"r")
allInsToHosList = ith_fhn.readlines()
ith_fhn.close()

for thisline1 in allInstanceList:
  thisline = thisline1.replace('\n','')
  if thisline.find("terminated") >= 0:
    insid = thisline.split(',')[0]

    for this_ith1 in allInsToHosList:
      this_ith = this_ith1.replace('\n','')
      if this_ith.find(insid) >= 0:
        zbxhostnm = this_ith.split(',')[1]
        print insid
        print zbxhostnm
##    zbxIpCtr.setIpAddr(zbxhostnm)

