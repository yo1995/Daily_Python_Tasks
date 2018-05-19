# -*- coding:utf-8 -*-

__author__ = 'cht'
'''
south-plus bbs checkin
credit: self-replica
https://github.com/yo1995/Daily_Python_Tasks/tree/master/Checkin_dianbook_kindbook
'''

import sys
import urllib
import re
import http.cookiejar
# import random
# import hashlib
# import time
# import datetime

from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
# from smtp_notifier import send_mail  # if needed, you could use my smtp_notifier script for sending email warning msg.


import logging
logger1 = logging.getLogger(__name__)
logger1.setLevel(level=logging.INFO)
handler = logging.FileHandler('southplus-log.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger1.addHandler(handler)


class SouthPlus(object):

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.cj = http.cookiejar.LWPCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)

    @staticmethod
    def _get_headers():
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        headers['Host'] = 'south-plus.net'
        headers['Origin'] = 'https://south-plus.net'
        # headers['Referer'] = 'https://south-plus.net/plugin.php?H_name-tasks.html'
        headers['Connection'] = 'keep-alive'
        headers['Cache-Control'] = 'max-age=0'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'
        # headers['Accept-Encoding']='gzip, deflate, br'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        return headers

    def _apply(self, html, mode):
        plugin_url = 'https://south-plus.net/plugin.php?H_name=tasks&action=ajax'
        soup = BeautifulSoup(html, "html.parser")
        # nowtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
        res = r"verifyhash = '(.*?)';"
        verifyhash = re.findall(res, str(soup), re.S | re.M)[0]
        # print(verifyhash)
        qiandao_url = plugin_url + '&actions=job&cid={mode}&verify={hash}'.format(mode=mode, hash=verifyhash)
        lingqv_url = plugin_url + '&actions=job2&cid={mode}&verify={hash}'.format(mode=mode, hash=verifyhash)
        try:
            req = urllib.request.Request(qiandao_url, headers=self._get_headers())
            response = urllib.request.urlopen(req)
            self.operate = self.opener.open(req)
            thepage = response.read()  # .decode('utf-8')
            result_soup = BeautifulSoup(thepage, "html.parser")
            # print(str(result_soup))
            apply_success_str = '请赶紧去完成任务吧'
            applied_str = '还没超过'
            if apply_success_str in str(result_soup):
                print('任务申请成功！')
            if applied_str in str(result_soup):
                print('任务已经申请，继续执行。')
            
            req = urllib.request.Request(lingqv_url, headers=self._get_headers())
            response = urllib.request.urlopen(req)
            self.operate = self.opener.open(req)
            thepage = response.read()  # .decode('utf-8')
            result_soup = BeautifulSoup(thepage, "html.parser")
            # print(str(result_soup))
            wait_str = '未申请任务'
            if wait_str in str(result_soup):
                already_log = '今日已经签到'
                print(already_log)
                logger1.warning('Warning! ' + already_log)
            completed_str = '已经完成'
            if completed_str in str(result_soup):
                if mode == 14:
                    success_log = '每周签到成功'
                    print(success_log)
                else:
                    success_log = '每日签到成功'
                    print(success_log)
                    logger1.info('Success: ' + success_log)
        except Exception:
            print('超级宽泛的异常处理，滚回检查你的设置！')
            logger1.error('Error!')

    def sign1(self, url, mode):
        # logger1.debug('start bbs sign : %s' % url)
        req = urllib.request.Request(url, headers=self._get_headers())
        response = self.opener.open(req)
        thepage = response.read()  # .decode('utf-8')
        self._apply(thepage, mode)

    def login_bbs(self, url, data):
        # logger1.debug( 'start bbs login : %s ' % url)
        req = urllib.request.Request(url=url, data=data, headers=self._get_headers())
        self.opener.open(req)

    def login_data(self):
        info = {}
        info['lgt'] = 0
        info['pwuser'] = self.name
        info['pwpwd'] = self.password
        info['cktime'] = 31536000
        info['step'] = 2
        info['hideid'] = 0
        info['forward'] = u'//south-plus.net/plugin.php?H_name-tasks.html'
        info['jumpurl'] = u'//south-plus.net/plugin.php?H_name-tasks.html'
        return urllib.parse.urlencode(info).encode("utf8")

    # obsolete
    @staticmethod
    def strip_tag(tag_str):
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        tag_str = re.sub(dr, '', tag_str)
        tag_str.replace(' ', '')
        return tag_str


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 sp-py3.py [mode:14/15], default daily mode = 15.')
        mode1 = 15
    else:
        mode1 = int(sys.argv[1])

    if mode1 != 14 and mode1 != 15:
        err_log = '错误的任务id！签到取消，请检查模式设置。'
        print(err_log)
        logger1.error(err_log)
        exit(1)

    host = 'https://south-plus.net/'
    '''
    weekday = datetime.datetime.now().weekday()
    sleep_time = (300 if (weekday > 4) else 0)
    sleep_time = sleep_time + 60 * random.random()
    print(sleep_time)
    time.sleep(sleep_time)  # 假装周末睡过头没有及时签到
    '''
    user_login = SouthPlus('[username]', '[password]')  # fill in your credentials here
    bbs_login_data = user_login.login_data()
    Login_Url = host + 'login.php?'
    user_login.login_bbs(Login_Url, bbs_login_data)
    check_url = host + 'plugin.php?H_name-tasks.html'
    user_login.sign1(check_url, mode1)  # mode 14 weekly/158hrs,15 daily/18hrs
