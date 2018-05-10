#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cht'
'''
TP-LINK router reboot
'''

import urllib
import base64
from urllib import request
from datetime import datetime
 
# IP for the routers
routers = [{'ip': '192.168.2.1', 'user': b'***', 'pwd': b'***'}]
page_url = '/userRpm/SysRebootRpm.htm'
 
if __name__ == '__main__':
    for router in routers:
        base_url = 'http://' + router['ip'] + page_url
        url = base_url + '?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7'
        auth = 'Basic ' + str(base64.b64encode(router['user'] + b':' + router['pwd']))
        print(datetime.now(), url)
        header = {'Referer': base_url, 'Authorization': auth}
        try:
            request = urllib.request.Request(url, None, header)
            response = urllib.request.urlopen(request)
            # reboot success state determination need to be added.
        except Exception as e:
            print('Reboot failed!', e)
            exit()

        print('Reboot succeeded!')
