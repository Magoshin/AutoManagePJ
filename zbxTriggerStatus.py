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

if __name__ == '__main__':

    param = sys.argv
    paramZabbixServer = param[1]
    paramHost = param[2]
    paramTrigger = param[3]
    paramSwitch = param[4]

    # status値を判定
    if paramSwitch == "on":
        chstatus = 0
    elif paramSwitch == "off":
        chstatus = 1
    else:
        print u"ステータスには on または off をすべて小文字で入力してください"
        sys.exit()

    api = ZabbixApi(paramZabbixServer, 'admin', 'zabbix')

    response = api.request('host.get',
                           {"output": "hostid",
                            "filter": {"host": paramHost}})
    response1 = response['result']

    # 返り値が空白か確認
    if not response1:
        print u"存在しないホストです"
        sys.exit()

    # ホストidを抽出
    response2 = str(response1)
    findhostid_pre = response2[14:-2]
    findhostid = findhostid_pre.lstrip('\'')

    triglist = api.request('trigger.get',
                           {"output": "triggerid",
                            "hostids": findhostid,
                            "filter": {"description": paramTrigger}})

    # トリガーIDを抽出
    trigRes1 = triglist['result']
    trigRes2 = str(trigRes1)
    findtrigid_pre1 = trigRes2.split(":")
    findtrigid_pre2 = findtrigid_pre1[1]
    findtrigid_pre3 = findtrigid_pre2.split("'")
    findtrigid = findtrigid_pre3[1]

    rescode = api.request('trigger.update',
                          {"triggerid": findtrigid,
                           "status": chstatus})

    if 'result' in rescode:
        print u"処理は成功しました"
        # 成功時の処理
        pass
    elif 'error' in rescode:
        print u"処理は失敗しました"
        # 失敗時の処理
        pass
    else:
        print u"予期しないエラーが発生しました"
        # 不具合時の処理
        pass
