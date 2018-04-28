# -*- coding:utf-8 -*-
#! python3

__author__ = 'cht'
'''
1point3acres bbs checkin
credits: 
- https://github.com/vpzlin/PyProjZ/blob/master/examples/Python%E6%BA%90%E7%A0%81%E5%8F%82%E8%80%83/pythonmaterial/scripts-shell/python%E8%AE%BA%E5%9D%9B%E8%87%AA%E5%8A%A8%E7%AD%BE%E5%88%B0%E7%94%A8bs4%E6%A8%A1%E5%9D%97.py
- https://github.com/JeffChern/1point3acres_AutoLogin
- https://github.com/wcyz666/MyScript/blob/master/1point3arcs.py
'''

import urllib
import re
import random
import hashlib
import logging
import time
import datetime
import http.cookiejar
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse

logging.basicConfig(filename='1point3acres-log.log', level=logging.INFO)


class yimu(object):

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.cj = http.cookiejar.LWPCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)

    def _getHeaders(self):
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers['Host'] = 'www.1point3acres.com'
        headers['Connection'] = 'keep-alive'
        headers['Cache-Control'] = 'max-age=0'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
        # headers['Accept-Encoding']='gzip, deflate, sdch'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        return headers

    def _say(self, html):
        soup = BeautifulSoup(html, "html.parser")
        qdxq = ['kx', 'ng', 'ym', 'wl', 'nu', 'ch', 'fd', 'yl', 'shuai']  # 签到心情列表
        nowtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间

        try:
            qd_form = soup.find_all(id="qiandao")[0]
            s_action = qd_form['action']
            # print('s_action is : %s' % s_action)
            inputes = soup.find_all("input")
            s_formhash = ''
            s_qdxq = random.choice(qdxq)
            s_qdmode = '1'
            for input in inputes:
                if input['name'] == 'formhash':
                    s_formhash = input['value']
                    break

            loginparams = {'formhash': s_formhash, 'qdxq': s_qdxq, 'qdmode': s_qdmode, 'todaysay': '今天把论坛帖子介绍给好基友了~'}
            req = urllib.request.Request(r'http://www.1point3acres.com/bbs/' + s_action, urllib.parse.urlencode(loginparams).encode("gbk"), headers=self._getHeaders())
            response = urllib.request.urlopen(req)
            self.operate = self.opener.open(req)
            thepage = response.read()  # .decode('utf-8')
            result_soup = BeautifulSoup(thepage, "html.parser")
            for c in result_soup.find_all("div", class_="c"):
                strlog = "签到状态：" + self.strip_tag(str(c)) + '，签到时间：' + nowtime
                print(strlog)
                logging.info(strlog)
        except IndexError:
            checkin_info = self.match_result(str(soup))
            str_log = self.strip_tag(str(checkin_info[0])) + '，' + self.name + "已累计签到: " + self.strip_tag(str(checkin_info[1])) + '天，本月签到' + self.strip_tag(str(checkin_info[2])) + '天，上次时间' + self.strip_tag(str(checkin_info[3]))
            print(str_log)
            logging.info(str_log)

    def sign(self, url):
        # logging.debug('start bbs sign : %s' % url)
        req = urllib.request.Request(url, headers=self._getHeaders())
        response = urllib.request.urlopen(req)
        self.opener.open(req)
        thepage = response.read() # .decode('utf-8')
        self._say(thepage)

    def login_bbs(self, url, data):
        # logging.debug( 'start bbs login : %s ' % url)
        req = urllib.request.Request(url=url, data=data, headers=self._getHeaders())
        self.opener.open(req)

    def login_data(self):
        # logging.debug(u'正在登陆 username : %s password : %s' % (self.name, self.password))
        # logging.debug(u'headers is : %s' % self._getHeaders())
        info = {}
        info['username'] = self.name
        info['password'] = self.process_md5(self.password)
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
        res = r'<h1 class="mt">(.*?)</h1>'
        mm[0] = re.findall(res, res_str, re.S | re.M)[0]
        res = r'您累计已签到:(.*?)天'
        mm[1] = re.findall(res, res_str, re.S | re.M)[0]
        res = r'您本月已累计签到:(.*?)天'
        mm[2] = re.findall(res, res_str, re.S | re.M)[0]
        res = r'您上次签到时间:(.*?)</font>'
        mm[3] = re.findall(res, res_str, re.S | re.M)[0]
        return mm

    @staticmethod
    def strip_tag(tag_str):
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        tag_str = re.sub(dr, '', tag_str)
        tag_str.replace(' ', '')
        return tag_str


if __name__ == '__main__':
    weekday = datetime.datetime.now().weekday()
    sleep_time = (300 if (weekday > 4) else 0)
    sleep_time = sleep_time + 60 * random.random()
    print(sleep_time)
    time.sleep(sleep_time)  # 假装周末睡过头没有及时签到
    userlogin = yimu('username', 'password')
    bbs_login_data = userlogin.login_data()
    Login_Url = "http://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    userlogin.login_bbs(Login_Url, bbs_login_data)
    userlogin.sign('http://www.1point3acres.com/bbs/dsu_paulsign-sign.html')
