## Description

A simple check in script for http://www.1point3acres.com/bbs/dsu_paulsign-sign.html

Based on the regular webpage request methods and procedures. Username and password are stored in the script as clear text, so be sure the file won't be exposed to public!

Post data, cookie and headers are constructed to meet the form requirements of that webpage.

一亩三分地签到脚本，采用Python3，代码结构简洁易懂。

### 20180428 v1.0

added python3 version.

To be noticed: the PASSWORD on 一亩三分地 is translated to md5 locally before submitting the log-in form.
Don't know if that will change someday in the future. If salt is added, more work would need to be done.

Works fine with 1point3acres 一亩三分地 check-in 签到 process.

Please use python3 and crontab to deploy and run periodically if needed.

### 使用方法

改写脚本中用户名和密码，直接运行或定时运行即可。将输出日志记录签到成功状态。~~运行有问题可自行debug~~
