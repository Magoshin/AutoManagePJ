# -*- coding: utf-8 -*-

import json
import urllib
import urllib2
import sys


class ZabbixApi(object):
    def __init__(self, host, user, password):
        user = "admin"
        password = "zabbix"

        self.request_id = 1
        self.host = host
        self.auth_token = self.request('user.login',
                                       {'user': user, 'password': password})
        self.auth_token = self.auth_token['result']

    def request(self, method, params, auth_token=None):
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

def hostStatusChange(hostnm, statuscode):

    paramZabbixServer = '172.31.16.60'

    api = ZabbixApi(paramZabbixServer, 'admin', 'zabbix')

    # hostid を調べる
    response = api.request('host.get',
                           {"output": "hostid",
                            "filter": {"host": hostnm}})

    # 存在チェックの後、ステータス変更
    if not response['result']:
        pass
    else:
        restr = response['result'][0]
        hostid = restr['hostid']
        # ホストのステータスを変更する
        response = api.request('host.update',
                               {"hostid": hostid,
                                "status": statuscode})
