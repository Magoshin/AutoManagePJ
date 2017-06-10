#!/usr/bin/env python
# -*- coding:utf-8 -*-

##import otrsTicketHandle as ctr_otrs_api
from otrsTicketHandle import OTRSApi

import json
import sys
import string
import os

if __name__ == "__main__":
  # チケット作成
  OT_ins = OTRSApi()
##  rtn = OT_ins.CreateTicket("test", "Problem" , "Miyake", "open", "3 normal", "testcust", "sub", "body")
##  print rtn

  # キュー内調査
##  rtn2 = OT_ins.Search("FailureNotifi")
##  print rtn2

  # チケット詳細
  rtn3 = OT_ins.GetTicket("FailureNotifi", 159)
  print rtn3
