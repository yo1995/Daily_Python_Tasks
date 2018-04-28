#! /usr/bin/env python
# coding:utf-8
import sys
import re
import requests
import logging
import time

# 配置日志文件和日志级别
logging.basicConfig(filename='SSR-log.log', level=logging.INFO)


def check(str):
    hasCheckIn = '<button id="checkin" class="btn btn-success  btn-flat">'
    noChecked = '<a class="btn btn-success btn-flat disabled" href="#">'
    yes = re.search(hasCheckIn, str)
    if yes == None:
        no = re.search(noChecked, str)
        if no == None:
            return -1  # 什么都没找到
        else:
            return 0  # 找到了“不能签到”
    else:
        return 1  # 找到了“签到”


def match_flows(str):
    res = r'<dl class="dl-horizontal">(.*?)</dl>'
    mm = re.findall(
        res, str, re.S | re.M)
    res = r'<dd>(.*?)</dd>'
    mm = re.findall(
        res, mm[0], re.S | re.M)
    return mm
    ## 这段代码是用于解决中文报错的问题


reload(sys)
sys.setdefaultencoding("utf8")
email = 'your@email'
password = 'yourpswd'
loginurl = 'https://ssr.0v0.cat/auth/login'
# 这行代码，是用来维持cookie的，你后续的操作都不用担心cookie，他会自动带上相应的cookie
s = requests.Session()
# 我们需要带表单的参数
loginparams = {'email': email, 'passwd': password, 'remember_me': 'ture'}
# post 数据实现登录
r = s.post(loginurl, data=loginparams)
# 验证是否登陆成功，抓取首页看看内容
r = s.get(loginurl)
res = check(r.content)  # 0=不能签到;1=可以签到;-1=什么都没找到;
if (res == 1):  # 可以签到
    checkinUrl = "https://ssr.0v0.cat/user/checkin"
    r = s.post(checkinUrl)
    r = s.get(loginurl)
lastFlows = match_flows(r.content)
nowtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前时间
str = nowtime + ',\t总流量：' + lastFlows[0] + ',\t已用流量：' + lastFlows[1] + ',\t剩余流量：' + lastFlows[2]
print str
logging.info(str)
