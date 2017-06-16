# -*- coding: utf-8 -*-

import json
import urllib
import urllib2
import sys
import boto3


class ZabbixApi(object):
    def __init__(self, host, user, password):
        """Zabbix API インスタンスを返す
        :param host: Zabbix サーバの IP アドレス
        :param user: Zabbix API のアクセスユーザ
        :param password: Zabbix API のアクセスユーザパスワード
        :return:
        """
        user = "admin"
        password = "zabbix"

        self.request_id = 1
        self.host = host
        self.auth_token = self.request('user.login',
                                       {'user': user, 'password': password})
        self.auth_token = self.auth_token['result']

    def request(self, method, params, auth_token=None):
        """Zabbix API にリクエストを送信する
        id は現行特に必要ないため単純にインクリメントした数値を代入している。

        :param method: Zabbix API のメソッド名
        :param params: Zabbix API のメソッドの引数
        :param auth_token: Zabbix API の認証トークン
        :return: JSON-RPC2.0 形式の応答
        """
        if hasattr(self, 'auth_token'):
            auth_token = self.auth_token
        headers = {"Content-Type": "application/json-rpc"}
        uri = "http://{0}/zabbix/api_jsonrpc.php".format(self.host)
        data = json.dumps({'jsonrpc': '2.0',
                           'method': method,
                           'params': params,
                           'auth': auth_token,
                           'id': self.request_id})
        request = urllib2.Request(uri, data, headers)
        self.request_id += 1
        return json.loads(urllib2.urlopen(request).read())

def setIpAddr(hostnm):
    paramZabbixServer = '172.31.16.60'

    api = ZabbixApi(paramZabbixServer, 'admin', 'zabbix')

    # hostid を調べる
    response = api.request('host.get',
                           {"output": "hostid",
                            "filter": {"host": hostnm}})
    restr = response['result'][0]
    hostid = restr['hostid']

    # interfaceid を調べる
    response = api.request('hostinterface.get',
                           {"output": "extend", "hostids": hostid})
    ifstr = response['result'][0]
    infid = ifstr['interfaceid']

    instanceListNm = "/home/ansible/pythonTools/data/instanceList.txt"
    fhn = open(instanceListNm, "r")
    allInstanceList = fhn.readlines()
    fhn.close()

    # IPアドレスを一覧から取得
    for insinfo in allInstanceList:
        if insinfo.find(hostnm) >= 0:
            ipaddr = insinfo.split(",")[4]
            break

    # IPアドレスを設定する
    response = api.request('hostinterface.update',
                           {"hostid": hostid,
                            "ip": ipaddr,
                            "interfaceid": infid})
