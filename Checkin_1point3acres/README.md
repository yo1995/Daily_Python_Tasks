## Description

![logo](http://www.1point3acres.com/bbs/static/image/common/logo.png)

A simple check in script for http://www.1point3acres.com/bbs/dsu_paulsign-sign.html

Based on the regular webpage request methods and procedures. Username and password are stored in the script as clear text, so be sure the file won't be exposed to public!

Post data, cookie and headers are constructed to meet the form requirements of that webpage.

一亩三分地签到脚本，采用Python3，代码结构简洁易懂。

## Versions

### 20180428 v1.0.0

- added python3 version.

To be noticed: the PASSWORD on 一亩三分地 is translated to md5 locally before submitting the log-in form.
Don't know if that will change someday in the future. If salt is added, more work would need to be done.

### 20180428 v1.0.1

- fixed gbk encoding issue

- 时间段内随机睡眠时间，降低非人类嫌疑

### 20180502 v1.0.2

- added email notification option

### 20180512 v1.0.3

- 重新修复gbk编码问题，防止提交数据出现乱码

### 20190417 v1.0.4

- 近期地里更新了登录方法，添加了验证码，故改为cookies验证方式。  
请将Chrome中cookies字段中的字符串保存为yimu-cookie.txt并与脚本置于同一目录下，或自行指定路径。

### 20190616

补充：目前可以放/bbs目录或者签到页面的cookie都可以~记一句以防后面忘了……

## 使用方法

Works fine with 1point3acres 一亩三分地 check-in 签到 process.

Please use python3 and crontab to deploy and run periodically if needed.

改写脚本中用户名和密码，直接运行或定时运行即可。将输出日志记录签到成功状态。~~运行有问题可自行debug~~
注明出处任意转载，但请低调使用，省得迭代~
如果喜欢烦请star，如有问题issue

## 未来可能添加



## 关键词

dsu_paulsign:sign | dsu_paulsign-sign.html | 一亩三分地 | 每日签到 | 【DSU】每日签到 Ver 4.8.1 © BranchZero
