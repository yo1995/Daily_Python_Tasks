## Description

![logo](http://muchongimg.xmcimg.com/data/emuch_bbs_images/portal/image/portal/logo.png)

A simple check in script for http://muchong.com/bbs/memcp.php?action=getcredit

Based on the regular webpage request methods and procedures. Username and password are stored in the script as clear text, so be sure the file won't be exposed to public!

Post data, cookie and headers are constructed to meet the form requirements of that webpage.

Also, to meet the 2-step verification requirement of that site, a simple parser of the arithmetic problem is designed. See in the script!

小木虫论坛签到脚本，采用Python3，代码结构简洁易懂。

由https://github.com/andyyelu/muchong_checkin 所启发，更改优化了其代码结构，并添加了少量容错处理。

## Versions

### 20180502 v1.0.0

- added python3 version.

## 使用方法

Works fine with http://muchong.com/bbs/ 小木虫论坛 check-in 签到 process.

Please use python3 and crontab to deploy and run periodically if needed.

改写脚本中用户名和密码，直接运行或定时运行即可。
将输出日志记录签到状态。~~运行有问题可自行debug~~
如有需要可配合repo内邮件通知插件一起使用。
注明出处任意转载，但请低调使用，省得迭代~
如果喜欢烦请star，如有问题issue

## 未来可能添加



## 关键词

小木虫 | 每日签到 | 小木虫论坛-学术科研互动平台 » 红包领取 | 领取每日红包
