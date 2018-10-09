# -*- coding:utf-8 -*-
__author__ = 'cht'


import smtplib
import time

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
# from email.mime.application import MIMEApplication


def send_mail(sender_address, sender_password, receiver_address, smtp_server, subject="无主题", smtp_port=25, body="测试邮件发送"):
    email_from = sender_address
    email_password = sender_password
    email_to = receiver_address  # still have issue in multi-CN character processing
    email_sub = subject

    msg = MIMEMultipart()
    # msg['From'] = Header("MyServer", 'utf-8')  # nickname
    # msg['To'] = Header("通知接收邮箱", 'utf-8')  # nickname
    from_header = Header("Robin.anonym", 'utf-8').encode()  # nickname
    to_header = Header("菁客工作人员", 'utf-8').encode()  # nickname
    anonym_address = 'robin@baidu.com'
    msg['From'] = formataddr([from_header, anonym_address])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
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
        print("Warning: 正在使用非安全的SMTP25端口。")
        smtp = smtplib.SMTP()
    try:
        smtp.connect(smtp_server, smtp_port)  # 使用的邮箱smtp服务器
        smtp.login(email_from, email_password)  # 邮箱登录
        smtp.sendmail(email_from, email_to, msg.as_string())  # 发送邮件内容
        smtp.quit()  # 关闭链接
        print("Success: 邮件已发送成功")
    except smtplib.SMTPException:
        print("Error: 邮件发送失败")


main_body = "工作人员您好，<br>" \
          "    在如下页面https://www.ajinga.com/applecampus/corporate/ 中我发现“北京邮电大学”被误写为“北京邮件大学”。烦请更正！<br>谢谢，"

# send_mail('email', 'pin', 'tomail', 'server', 'subject', 465, main_body)
input("任意键结束")


