## Description

![logo](http://n.sinaimg.cn/translate/20170920/ywf8-fykymue7425851.gif)

A simple add-on script for sending logging information to designated email address. Easy to use when you need to acquire warning status of your check-in scripts.

## Versions

### 20180502 v1.0.0

- added python3 version.

- added SSL support choice

## Usage

1. download and put this script within the dir of your check-in script
2. in your script import it:
'''python
from smtp_notifier import send_mail
'''
3. call it. e.g.:
'''python
send_mail(sender_address, sender_password, receiver_address, smtp_server, "subjectXXX", 465, "bodyYYY"):
'''
