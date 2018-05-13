#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cht'
'''
TP-LINK router reboot, especially for Archer C7
'''

import urllib
import base64
import re
from urllib import request
from datetime import datetime
from bs4 import BeautifulSoup

# IP for the routers
routers = [{'ip': '192.168.2.1', 'user': b'yours', 'pwd': b'yours'}]
# page_url = '/userRpm/SysRebootRpm.htm'
page_url = '/userRpm/LoginRpm.htm?Save=Save'

if __name__ == '__main__':
    for router in routers:
        base_url = 'http://' + router['ip'] + page_url
        auth_value = base64.b64encode(router['user'] + b':' + router['pwd'])
        auth = 'Basic ' + auth_value.decode()
        print(datetime.now(), base_url, auth)
        header = {'Referer': base_url, 'Cookie': 'Authorization=' + auth}
        try:
            # first simulate login
            request = urllib.request.Request(base_url, None, header)
            response = urllib.request.urlopen(request)
            page = response.read()
            soup = BeautifulSoup(page, "html.parser")
            # make the reboot link
            res = 'http://' + router['ip'] + '/' + '(.*?)/userRpm/Index.htm'
            mm = re.findall(res, str(soup), re.S | re.M)[0]  # get the strange hash?
            reboot_url = 'http://' + router['ip'] + '/' + mm + '/userRpm/SysRebootRpm.htm' + '?Reboot=Reboot'
            #
            request = urllib.request.Request(reboot_url, None, header)
            response = urllib.request.urlopen(request)
            page = response.read()
            soup = BeautifulSoup(page, "html.parser")
            # print(str(soup))
            # reboot success state determination need to be added.
        except Exception as e:
            print('Reboot failed!', e)
            exit()

        print('Reboot succeeded! Now setting time zone!')
        # more to add: set time zone,


