## Description

![logo](http://dianbook.cc/template/xc_lalala/src/images/logo.png)

inspired by https://github.com/hldh214/dsu_autosign/tree/master

A simple check in script for http://dianbook.cc/plugin.php?id=k_misign:sign

Based on the regular webpage request methods and procedures. Username and password are stored in the script as clear text, so be sure the file won't be exposed to public!

Post data, cookie and headers are constructed to meet the form requirements of that webpage.

点书网/益书网(关闭)签到脚本，采用Python3，代码结构简洁易懂。

## Versions

### 20180429 v1.0.0

- added python3 version.

### 20180501 v1.0.1

- added assertion for login failure

### 20180523 v1.0.3

- 改进了编码解码方式，兼容性更好。

## 使用方法

Please use python3 and crontab to deploy and run periodically if needed.

e.g. ~ crontab -e
0 12 * * * python3 /home/[youruser]/dianbook-py3.py

## 关键词

k_misign:sign | 【Discuz插件】百变小米每日签到 | 点书网 | 每日签到 | http://www.gezhongshu.com
