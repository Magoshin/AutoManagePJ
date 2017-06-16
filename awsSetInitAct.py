#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import boto3
import json
import shutil
import os
import subprocess

client = boto3.client('ec2')
res = client.describe_instances

# parameter define
instanceListNm = "/home/ansible/pythonTools/data/instanceList.txt"
tmpInitlist = "/home/ansible/pythonTools/data/tmpInitlist"
playbookdir = "/home/ansible/playbook/"
init_inventry = "/home/ansible/init_inventry"
za_invent = "/home/ansible/zbxAgent_inventry"

initcnt = 0
initcnt = num_lines = sum(1 for line in open(tmpInitlist))

if initcnt > 0:
    # initinventryファイルの生成
    fhn = open(init_inventry, "w")
    fhn.write("[init]\n")
    fhn.close()

    cmd = "cat " + tmpInitlist + " >> " + init_inventry
    proc = subprocess.call(cmd, shell=True)

    fhn = open(init_inventry, "a")
    fhn.write("[all:vars]\n")
    fhn.write("ansible_ssh_port=22\n")
    fhn.write("ansible_ssh_user=ec2-user\n")
    fhn.write("ansible_ssh_private_key_file=\
        /home/ansible/.ssh/ec2_private.key\n")
    fhn.close()

    # inituser作成コマンドの発行
    cmd = "ansible-playbook -i " + init_inventry \
        + " --user ec2-user " + playbookdir \
        + "inituser/addInituser.yml"
    proc = subprocess.call(cmd, shell=True)

    # Zabbix Agent を入れる
    fhn = open(za_invent, "w")
    fhn.write("[zabbix-agent]\n")
    fhn.close()

    cmd = "cat " + tmpInitlist + " >> " + za_invent
    proc = subprocess.call(cmd, shell=True)

    fhn = open(za_invent, "a")
    fhn.write("[all:vars]\n")
    fhn.write("ansible_ssh_port=22\n")
    fhn.write("ansible_ssh_user=inituser\n")
    fhn.write("ansible_ssh_private_key_file=\
        /home/ansible/.ssh/inituser_id_rsa\n")
    fhn.close()

    # zabbix-agentインストールコマンドの発行
    cmd = "ansible-playbook -i" + za_invent \
        + " --user inituser " + playbookdir \
        + "zabbix/zabbixAgent_install.yml"
    proc = subprocess.call(cmd, shell=True)

    # tag 変更 init -> ready
    # aws ec2 create-tag でタグを変更。無念。。
    fhn = open(instanceListNm, "r")
    ld = open(tmpInitlist, "r")
    allInstanceList = fhn.readlines()
    allInitList = ld.readlines()
    for tmpInitIP in allInitList:
        thisip = tmpInitIP.replace("\n", "")
        for insinfo in allInstanceList:
            if insinfo.find(thisip) >= 0:
                targetid = insinfo.split(",")[0]
                cmd = "aws ec2 create-tags --resources " + targetid \
                    + " --tags Key=Name,Value=ready"
                proc = subprocess.call(cmd, shell=True)

# 一時インベントリを削除
if os.path.isfile(init_inventry):
    os.remove(init_inventry)
if os.path.isfile(za_invent):
    os.remove(za_invent)
