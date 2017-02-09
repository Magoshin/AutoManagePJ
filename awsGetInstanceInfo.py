#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import boto3
import json
import shutil
import os
import subprocess
import re

import zbxHostStatus as statCtr
import zbxHostDelete as delCtr

client = boto3.client('ec2')
res = client.describe_instances

## parameter define
instanceListNm = "/home/ansible/pythonTools/data/instanceList.txt"
tmpInitlist = "/home/ansible/pythonTools/data/tmpInitlist"
insToHostNm = "/home/ansible/pythonTools/data/insToHostnmList.txt"

fhn = open(instanceListNm,"w")
ith_fhn = open(insToHostNm,'r')

## insToHostnmList.txt の永続名前解決一覧
allinsToHost = ith_fhn.readlines()
ith_fhn.close()

# 一時init対象一覧を開く
til = open(tmpInitlist,"a")

for i in boto3.resource('ec2').instances.iterator():
  pubip = str(i.public_ip_address)
  privip = str(i.private_ip_address)
  ##tagname = str(i.tags[0]['Value'])
  tagname = i.tags[0]['Value']
  dnsname = i.private_dns_name
  if dnsname != "":
    zbxhostnm = dnsname.split('.')[0]
  else:
    zbxhostnm = ""

  initcnt = 0
  # tag に init表記あり、statusが"running"の場合、tmpInitlistにIPを書き込む
  if tagname == "init" and i.state['Name'] == "running":
    til.write(privip + "\n")
    initcnt += 1

  # tag に init表記なし、statusが"running"の場合、監視有効化
  if tagname != "init" and i.state['Name'] == "running":
    statCtr.hostStatusChange(zbxhostnm,0)

  # 停止したインスタンスは、Zabbixホストも無効化
  if i.state['Name'] == "stopped":
    statCtr.hostStatusChange(zbxhostnm,1)

  # インスタンスIDとホスト名の紐付けリスト
  # ホスト削除の際に絶対必要

  # insToHostnmList.txt(永続インスタンスIDとホスト名の紐付けリスト)に存在するかチェック
  matchOBJ_flag = 0
  for insToHostInfo1 in allinsToHost:
    insToHostInfo = insToHostInfo1.replace('\n','')
    matchOBJ = re.match(i.id , insToHostInfo)
    if matchOBJ:
      matchOBJ_flag = 1
      break

  # insToHostnmList.txtに存在しない且つstatusが"terminated"でないものは追記
  if matchOBJ_flag != 1 and i.state['Name'] != "terminated":
    ith_fhn = open(insToHostNm,'a')
    ith_fhn.write(i.id + ',' + dnsname + "\n")
    ith_fhn.close()

  # インスタンスリアルタイムリストを更新
  printdata = i.id + ',' + dnsname + ',' + i.state['Name'] + ',' + pubip + ',' + privip + ',' + tagname + "\n"
  fhn.writelines(printdata)
fhn.close()
til.close()

# 一旦ファイルを閉じた後に削除処理
fhn = open(instanceListNm,"r")
allInstanceList = fhn.readlines()
fhn.close()

ith_fhn = open(insToHostNm,'r')
allinsToHost = ith_fhn.readlines()
ith_fhn.close()

for deldata in allInstanceList:
  terminStus = deldata.split(',')[2].replace('\n','')
  if terminStus.find("terminated") >= 0:
    terminId = deldata.split(',')[0].replace('\n','')
    for insToHost in allinsToHost:
      this_hostId = insToHost.split(',')[0].replace('\n','')
      # terminated 対象のインスタンスIDからホスト名を調査
      if this_hostId.find(terminId) >= 0:
        targHostnm1 = insToHost.split(',')[1].replace('\n','')
        targHostnm = targHostnm1.split('.')[0]
##        print targHostnm
        # zabbixホスト削除
        delCtr.hostDelete(targHostnm)

