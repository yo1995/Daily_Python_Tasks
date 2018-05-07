# -*- coding:utf-8 -*-
__author__ = 'cht'

'''
https://bbs.byr.cn/#!article/BUPTNet/91465
'''

import smtplib
import time

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
# from email.mime.application import MIMEApplication
# logging.basicConfig(filename='smtp.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARNING)
handler = logging.FileHandler('smtp-log.log')
handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_mail(sender_address, sender_password, receiver_address, smtp_server, subject="脚本异常报告", smtp_port=25, body="测试邮件发送"):
    email_from = sender_address
    email_password = sender_password
    email_to = receiver_address  # still have issue in multi-CN character processing
    email_sub = subject + str(time.strftime("%Y/%m/%d", time.localtime()))

    msg = MIMEMultipart()
    # msg['From'] = Header("MyServer", 'utf-8')  # nickname
    # msg['To'] = Header("通知接收邮箱", 'utf-8')  # nickname
    from_header = Header("MyServer", 'utf-8').encode()  # nickname
    to_header = Header("通知接收邮箱", 'utf-8').encode()  # nickname
    msg['From'] = formataddr([from_header, sender_address])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr([to_header, email_to])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = Header(email_sub, 'utf-8')
    # 邮件主体内容
    # 邮件正文内容  "plain","html"
    mail_body = body
    msg.attach(MIMEText(mail_body, 'html', 'utf-8'))
    # 构造附件，传送当前目录下的 文件
    # att = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
    # att["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    # att["Content-Disposition"] = 'attachment; filename="TestCase.xls"'
    # msg.attach(att)

    if smtp_port == 465:
        smtp = smtplib.SMTP_SSL()  # nowadays most SMTP servers prefer SSL(port465) connections for safety
    else:
        logging.warning("正在使用非安全的SMTP25端口。")
        smtp = smtplib.SMTP()
    try:
        smtp.connect(smtp_server, smtp_port)  # 使用的邮箱smtp服务器
        smtp.login(email_from, email_password)  # 邮箱登录
        smtp.sendmail(email_from, email_to, msg.as_string())  # 发送邮件内容
        smtp.quit()  # 关闭链接
        print("Success: 邮件已发送成功")
    except smtplib.SMTPException:
        print("Error: 邮件发送失败")
        logging.error("邮件发送失败。")


# send_mail()

