#!/usr/bin/env python
# -- coding=utf8 --
__author__ = 'InMath'
import ConfigParser
import smtplib
import json.encoder
from email.message import Message

def iniconfigparser(inifilename):
    """
    解析配置文件工具方法

    :param inifilename: string
    :return: RawConfigParser
    """
    _cp = ConfigParser.ConfigParser()
    _databasef = file(inifilename)
    _cp.readfp(_databasef)
    return _cp


def sendmail(subject, from_addr, to_addrs):
    """
    发送电子邮件工具方法

    """
    msg = Message()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ",".join(to_addrs)

    s = smtplib.SMTP('smtp.126.com')
    s.ehlo("smtp.126.com")
    # s.login('inmath@126.com', 'bzvohpkupkaofdgb')
    print msg.as_string()
    s.sendmail(from_addr, to_addrs, msg.as_string())
    s.quit()
