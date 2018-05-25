# -*- coding:utf-8 -*-

__author__ = 'cht'
'''
dianbook.cc bbs checkin
http://dianbook.cc/plugin.php?id=k_misign:sign
http://www.gezhongshu.com/forum.php
credits: 
- https://github.com/yo1995/Daily_Python_Tasks/tree/master/Checkin_1point3acres
0 12 * * * python3 /home/[]/dianbook-py3.py
'''

import urllib
import re
import requests
import hashlib
import logging
import time
import http.cookiejar
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
from smtp_notifier import send_mail

logging.basicConfig(filename='dianbook-log.log', level=logging.INFO)


class dianbook(object):

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.cj = http.cookiejar.LWPCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)

    def _say(self, html):
        soup = BeautifulSoup(html, "html.parser")
        nowtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
        try:
            assert('您今天还没有签到' in str(soup))  # v1.0.1 add assertion failure # v1.0.2 update

            re_hash = re.compile(r'action=logout&amp;formhash=(.*?)">')
            s_formhash = re_hash.findall(str(soup))[0]
            qiandao_url = 'http://dianbook.cc/plugin.php?id=k_misign:sign&operation=qiandao&formhash={0}'.format(s_formhash)
            qiandao_url = qiandao_url + '&from=insign'
            print(qiandao_url)
            check_url = 'http://dianbook.cc/plugin.php?id=k_misign:sign'
            req = urllib.request.Request(qiandao_url, headers=self._get_headers())
            urllib.request.urlopen(req)  # check in
            req2 = urllib.request.Request(check_url, headers=self._get_headers())
            response = urllib.request.urlopen(req2)
            self.operate = self.opener.open(req2)
            thepage = response.read()  # .decode('utf-8')
            result_soup = BeautifulSoup(thepage, "html.parser")
            # btnvisited = result_soup.find_all('span', class_='btn btnvisted')
            checkin_info = self.match_result(str(result_soup))
            str_log = self.strip_tag(
                "签到成功！排名：" + self.strip_tag(str(checkin_info[0]))) + '，' + self.name + "已累计签到: " + self.strip_tag(
                str(checkin_info[1])) + '天，连续签到' + self.strip_tag(str(checkin_info[2])) + '天，本次奖励' + self.strip_tag(
                str(checkin_info[3]) + '点券' + nowtime)
            print('签到成功！' + nowtime)
            logging.info(str_log)
            return True
        except (IndexError, AssertionError):
            err_msg = '签到错误！可能是已签到或未到时间。'
            print(err_msg + nowtime)
            logging.error(err_msg + self.name + nowtime)
            return False

    def sign(self, url):
        # logging.debug('start bbs sign : %s' % url)
        req = urllib.request.Request(url, headers=self._get_headers())
        response = urllib.request.urlopen(req)
        self.opener.open(req)
        thepage = response.read().decode('utf-8', errors='replace')
        return self._say(thepage)

    def login_bbs(self, url, data):
        # logging.debug( 'start bbs login : %s ' % url)
        req = urllib.request.Request(url=url, data=data, headers=self._get_headers())
        self.opener.open(req)

    def login_data(self):
        # logging.debug(u'正在登陆 username : %s password : %s' % (self.name, self.password))
        # logging.debug(u'headers is : %s' % self._get_headers())
        info = {}
        info['username'] = self.name
        info['password'] = self.password
        info['cookietime'] = 2592000
        info['quickforward'] = u'yes'
        info['handlekey'] = u'ls'
        return urllib.parse.urlencode(info).encode("utf8")

    @staticmethod
    def process_md5(password):
        m = hashlib.md5()
        m.update(password.encode("utf8"))
        return m.hexdigest()

    @staticmethod
    def match_result(res_str):
        mm = {}
        res = r'id="qiandaobtnnum" type="hidden" value="(.*?)"/>'
        #'您的签到排名：(.*?)</div>'
        mm[0] = re.findall(res, res_str, re.S | re.M)[0]
        res = r'id="lxtdays" type="hidden" value="(.*?)"/>'
        mm[1] = re.findall(res, res_str, re.S | re.M)[0]
        res = r'id="lxdays" type="hidden" value="(.*?)"/>'
        mm[2] = re.findall(res, res_str, re.S | re.M)[0]
        res = r'id="lxreward" type="hidden" value="(.*?)"/>'
        mm[3] = re.findall(res, res_str, re.S | re.M)[0]
        return mm

    @staticmethod
    def strip_tag(tag_str):
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        tag_str = re.sub(dr, '', tag_str)
        tag_str.replace(' ', '')
        return tag_str

    @staticmethod
    def _get_headers():
        headers = {}
        headers['User-Agent'] = u'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        headers['Host'] = u'dianbook.cc'
        headers['Connection'] = u'keep-alive'
        headers['Cache-Control'] = u'max-age=0'
        headers['Accept-Language'] = u'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'
        # headers['Accept-Encoding'] = u'gzip, deflate'
        headers['Accept'] = u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        return headers


if __name__ == '__main__':
    userlogin = dianbook('aaaaaa', '123456')  # 'username', 'password'
    bbs_login_data = userlogin.login_data()
    Login_Url = "http://dianbook.cc/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    userlogin.login_bbs(Login_Url, bbs_login_data)
    if not userlogin.sign('http://dianbook.cc/plugin.php?id=k_misign:sign'):
        time.sleep(60)  # once the time of website was late by 1 minute. add to avoid this circumstance
        if not userlogin.sign('http://dianbook.cc/plugin.php?id=k_misign:sign'):
            send_mail('from', 'pwd', 'to', 'server', "点书网异常报告", 465, '签到错误！已尝试两次签到未能成功。')
        else:
            print('success!')
    else:
        print('success!')
