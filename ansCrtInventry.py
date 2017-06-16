#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import string
import os
import subprocess


# Functions
def crtInventry(inilist):

    filenm = "/home/ansible/init_inventry"

    fhn = open(filenm, "w")
    fhn.write("[init]\n")
    fhn.write(inilist + "\n")
    fhn.close()

    # ファイルの連結
    cmd = "cat " + inilist + " >> " + filenm
    print cmd
    proc = subprocess.call(cmd, shell=True)

    return 0
