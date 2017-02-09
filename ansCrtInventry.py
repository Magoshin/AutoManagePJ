#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import string
import os

import subprocess

### Functions
def crtInventry(inilist):

  filenm = "/home/ansible/init_inventry"

  fhn = open(filenm,"w")
  fhn.write("[init]\n")
  fhn.write(inilist + "\n")
  fhn.close()

  # ファイルの連結
  cmd = "cat " + inilist + " >> " + filenm
  print cmd
  proc = subprocess.call( cmd , shell=True)

##  fhn = open(filenm,"a")
##  fhn.write("[all:vars]\n")
##  fhn.write("ansible_ssh_port=22\n")
##  fhn.write("ansible_ssh_user=ec2-user\n")
##  fhn.write("ansible_ssh_private_key_file=/home/ansible/.ssh/ec2_private.key\n")

##  fhn.close()

  return 0

