# -*- coding:utf-8 -*-
#! python3

__author__ = 'cht'
'''
小木虫 每日签到 muchong.com bbs checkin
credits: 
- https://github.com/andyyelu/muchong_checkin
'''

import re
import logging
import urllib
import http.cookiejar

from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from datetime import datetime
# from smtp_notifier import send_mail

logging.basicConfig(filename='muchong-log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MUCHONG_USERNAME = 'aaa'  # write your username and password here
MUCHONG_PASSWORD = 'bbb'


class MuChong(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cj = http.cookiejar.LWPCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)

    @staticmethod
    def _get_headers():
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        headers['Host'] = 'muchong.com'
        headers['Connection'] = 'keep-alive'
        # headers['Cache-Control'] = 'max-age=0'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'
        # headers['Accept-Encoding']='gzip, deflate, sdch'
        # headers['Origin'] = 'http://muchong.com'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        return headers

    def login(self):
        login_url = 'http://muchong.com/bbs/logging.php?action=login'
        req = urllib.request.Request(login_url, headers=self._get_headers())
        resp = urllib.request.urlopen(req)
        result_soup = BeautifulSoup(resp.read(), "html.parser")
        my_formhash = re.search(r'name="formhash" type="hidden" value="(\w{8})"', str(result_soup)).group(1)
        login_t = re.search(r't=(\d{10})', str(result_soup)).group(1)
        login_url = 'http://muchong.com/bbs/logging.php?action=login&t='+login_t
        my_data = {'formhash': my_formhash,
                   'refer': '',
                   'username': self.username,
                   'password': self.password,
                   'cookietime': '31536000',
                   'loginsubmit': '提交'}
        login_req = urllib.request.Request(login_url, data=urllib.parse.urlencode(my_data).encode("utf8"), headers=self._get_headers())
        login_result = urllib.request.urlopen(login_req)
        result_soup = BeautifulSoup(login_result.read(), "html.parser")
        verify_calc = re.search(u'问题：(\d+)(\D+)(\d+)等于多少?', str(result_soup))
        number1 = int(verify_calc.group(1))
        number2 = int(verify_calc.group(3))
        if verify_calc.group(2) == '加':
            my_answer = number1 + number2
        elif verify_calc.group(2) == '减':
            my_answer = number1 - number2
        elif verify_calc.group(2) == '乘以':
            my_answer = number1 * number2
        else:
            my_answer = number1 / number2

        my_post_sec_hash = re.search(r'name="post_sec_hash" type="hidden" value="(\w+)"', str(result_soup)).group(1)
        my_new_data = {'formhash': my_formhash,
                       'post_sec_code': int(my_answer),
                       'post_sec_hash': my_post_sec_hash,
                       'username': self.username,
                       'loginsubmit': '提交'}
        login_req = urllib.request.Request(login_url, data=urllib.parse.urlencode(my_new_data).encode("gbk"), headers=self._get_headers())
        self.opener.open(login_req)

    def sign(self):
        credit_url = 'http://muchong.com/bbs/memcp.php?action=getcredit'
        req = urllib.request.Request(credit_url, headers=self._get_headers())
        resp = self.opener.open(req)
        result_soup = BeautifulSoup(resp.read(), "html.parser")
        try:
            if u'您现在的金币数' in str(result_soup):
                coins_number = result_soup.find('span', {'style': 'color:red;font-weight:bold;font-size:20px;'})
                str_log = '今天已经签到！' + '目前的金币数是：%s.' % self.strip_tag(str(coins_number))
                print(str_log)
                logging.info(str_log)
            elif u'您还没有登录' in str(result_soup):
                str_log = '登录异常，没有成功登录！'
                print(str_log)
                logging.warning(str_log)
            else:
                credit_formhash = result_soup.find('input', {'name': 'formhash'})['value']
                credit_data = {'formhash': credit_formhash,
                               'getmode': '1',
                               'message': '',
                               'creditsubmit': '领取红包'}
                sign_req = urllib.request.Request(credit_url, data=urllib.parse.urlencode(credit_data).encode("gbk"),
                                                   headers=self._get_headers())
                resp = self.opener.open(sign_req)
                result_soup = BeautifulSoup(resp.read(), "html.parser")
                get_coins_number = result_soup.find('span', {'style': 'color:red;font-weight:bold;font-size:30px;'})
                coins = result_soup.find('span', {'style': 'color:red;font-weight:bold;font-size:20px;'})
                str_log = '本次登录成功！时间：%s. 金币数：%s. 总金币数：%s.\n' % (
                           datetime.now(), self.strip_tag(str(get_coins_number)), self.strip_tag(str(coins)))
                print(str_log)
                logging.info(str_log)
        except Exception as e:
            str_log = '签到失败！'
            print('签到失败', e)
            logging.error(str_log)
            # send_mail(blablabla)

    @staticmethod
    def strip_tag(tag_str):
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        tag_str = re.sub(dr, '', tag_str)
        tag_str.replace(' ', '')
        return tag_str


if __name__ == '__main__':
    user_login = MuChong(MUCHONG_USERNAME, MUCHONG_PASSWORD)
    user_login.login()
    user_login.sign()
