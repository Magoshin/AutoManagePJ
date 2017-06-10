#!/usr/bin/env python
# -*- coding:utf-8 -*-

##################################################################################################
####  
#### argv 1 -> hostname : 障害発生ホスト
#### argv 2 -> event_date : 障害検知日
#### argv 3 -> event_time : 障害検知時刻
#### argv 4 -> trigger_nsev : 障害深刻度
####                          0:Not classified 1:Information 2:Warning 3:Average 4:High 5:Disaster
#### argv 5 -> trigger_val : ステータス値
####                          0:OK 1:PROBLEM
#### argv 6 -> trigger_name : 発生障害名
##################################################################################################
from otrsTicketHandle import OTRSApi
from tocaroCallHandle import TocaroApi
import json
import sys
import string
import os

if __name__ == "__main__":
  # parameter
  param = sys.argv
  hostname = param[1]
  event_date = param[2]
  event_time = param[3]
  trigger_nsev = param[4]
  trigger_val = param[5]  
  trigger_name = param[6]

  # easy debug
  debugflag = 0
  if debugflag == 1:
    fd = open('/home/ansible/pythonTools/log/otrs.log', 'a') 
    fd.write("**************************\n")
    fd.write("hostname= "+ hostname + "\n")
    fd.write("event_date= "+ event_date + "\n")
    fd.write("event_time= "+ event_time + "\n")
    fd.write("trigger_nsev= "+ trigger_nsev + "\n")
    fd.write("trigger_val= "+ trigger_val + "\n")
    fd.write("trigger_name= "+ trigger_name + "\n")
    fd.close()  
  
  # 深刻度とOTRS優先度の紐づけ
  ot_priority = "3 normal"
  ot_sev = "軽度の障害"
  if trigger_nsev == 1:
    ot_priority = "1 very low"
    ot_sev = "情報"
  elif trigger_nsev == 2:
    ot_priority = "2 low"
    ot_sev = "警告"
  elif trigger_nsev == 3:
    ot_priority = "3 normal"
    ot_sev = "軽度の障害"
  elif trigger_nsev == 4:
    ot_priority = "4 high"
    ot_sev = "重度の障害"
  elif trigger_nsev == 5:
    ot_priority = "5 very high"
    ot_sev = "致命的な障害"

  ### ローカルファイルへの吐き出し
  zabbix_eventlog = "/var/log/zabbix/zabbix_event.log"
  log_messages = event_date + " " + event_time + " " + ot_sev + " " + hostname + " " + trigger_name
  with open('/var/log/zabbix/zabbix_event.log','a') as fh:
    fh.write(log_messages + '\n')

  ### OTRS 連携
  # インシデント情報の加工
  title = "Failure was detected in the ZBX"
  type = "Problem"
  queue = "FailureNotifi"
  state = "new"  
  priority = ot_priority
  customer_user = "testcust"
  otrs_subject = hostname + " : " + trigger_name
  body = "ZBX サーバで障害を検知しました。\n\n" + "発生日時：" + event_date + " " + event_time + "\n" + "発生ホスト：" + hostname + "\n" + "障害内容：" + trigger_name + "\n" + "深刻度：" + ot_sev + "\n\n" + "運用手順に従い、対応を開始してください。"

  # インスタンス生成
  OT_ins = OTRSApi()
  # OTRSでチケット作成
  newid = OT_ins.CreateTicket(title, type, queue, state, priority, customer_user, otrs_subject, body)

  ### Tocaro 連携
  tc_title = otrs_subject
  ticket_url = "http://52.199.253.24/otrs/index.pl?Action=AgentTicketZoom;TicketID=" + newid
  value = "Check the Failure information in " + ticket_url
  Tc_ins = TocaroApi()

  ## debug
  if debugflag == 1:
    fd = open('/home/ansible/pythonTools/log/otrs.log', 'a')
    fd.write("tc_title= "+ tc_title + "\n")
    fd.write("value= "+ value + "\n")
    fd.close()

  # Tocaroにメッセージを通知
  rtn3 = Tc_ins.sendMessage(tc_title, value)

  if debugflag == 1:
    fd = open('/home/ansible/pythonTools/log/otrs.log', 'a')
    fd.write("tocaro= "+ rtn3 + "\n")
    fd.close()
