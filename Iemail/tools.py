# -- coding=utf8 --
__author__ = 'InMath'
import smtplib
from email.message import Message


def sendmail(subject, from_addr, to_addrs):
    """
    发送电子邮件工具方法

    :param subject:   string   邮件主题
    :param from_addr: string   邮件发送地址
    :param to_addrs:  list     邮件接收地址
    """
    msg = Message()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ",".join(to_addrs)

    s = smtplib.SMTP('smtp.126.com')
    s.ehlo("smtp.126.com")
    s.login('inmath@126.com', 'bzvohpkupkaofdgb')
    s.sendmail(from_addr, to_addrs, msg.as_string())
    s.quit()
