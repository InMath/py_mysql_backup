#!/usr/bin/env python
# -- coding=utf-8 --
__author__ = 'InMath'
import os
import time
import sys
import subprocess as sbp
from BackupUtil import iniconfigparser

cp = iniconfigparser("database.ini")
dbuser = cp.get("database", "user")
dbpass = cp.get("database", "password")
now = time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))
increment_root_path = cp.get("backup", "increment_root_path")  # 增量文件根目录
full_root_path = cp.get("backup", "full_root_path")  # 全备文件根目录
full_store_dir = ""  # 全量备份文件
increment_base_dir = ""  # 增备文件基础目录
increment_store_dir = ""  # 增备文件
backup_mysql_cnf = cp.get("database", "backupconfigpath")  # 备份恢复mysql配置文件
if not os.path.exists(backup_mysql_cnf):
    print "备份恢复mysql配置文件不存在，请检查您的文件配置"
    exit(0)
if not os.path.exists(full_root_path):
    print "全备文件根目录不存在，请检查您的文件配置"
    exit(0)
if not os.path.exists(increment_root_path):
    print "增量文件根目录不存在，请检查您的文件配置"
    exit(0)

# 寻找最新的全量备份文件
tmp = 0
for filepath in os.listdir(full_root_path):
    if os.path.isdir(full_root_path + '/' + filepath) and tmp < int(filepath):
        tmp = int(filepath)
if tmp == 0:
    print "全量备份文件不存在！无法完成数据库恢复--！"
    exit(0)
full_store_dir = full_root_path + '/' + str(tmp)


# 寻找增量备份目录
increment_base_dir = increment_root_path + '/base_' + str(tmp)
increment_dir_list = os.listdir(increment_base_dir)
if not os.path.isdir(increment_base_dir) or not increment_dir_list:
    print "增量备份文件不存在！，程序将基于全量文件进行数据恢复......"
    cmd = "innobackupex --apply-log --use-memory=512M %s" % (full_store_dir,)
    sbp.call(cmd, shell=True)
    cmd = "innobackupex --defaults-file=%s --copy-back %s" % (backup_mysql_cnf, full_store_dir)
    sbp.call(cmd, shell=True)
    exit(0)
else:
    # 执行增量备份恢复流程
    increment_dir_list.sort()
    cmd = "innobackupex --apply-log --redo-only %s " \
          "--use-memory=512M --user=%s --password=%s" % (full_store_dir, dbuser, dbpass)
    sbp.call(cmd, shell=True)
    for item in increment_dir_list:
        increment_store_dir = increment_base_dir + '/' + item
        if not os.path.isdir(increment_store_dir):
            print "备份失效！失效文件路径为：" + increment_store_dir
            exit(0)
        #elif item == increment_dir_list[-1]:
        #    cmd = "innobackupex --apply-log %s incremental-dir=%s" % (full_store_dir, increment_store_dir)
        else:
            cmd = "innobackupex --apply-log --redo-only %s --incremental-dir=%s " \
                  "--use-memory=512M --user=%s --password=%s" % (full_store_dir, increment_store_dir, dbuser, dbpass)
            print cmd
            sbp.call(cmd, shell=True)
    cmd = "innobackupex --apply-log %s " \
          "--use-memory=512M --user=%s --password=%s" % (full_store_dir, dbuser, dbpass)
    cmd = "innobackupex --defaults-file=%s --copy-back %s" % (backup_mysql_cnf, full_store_dir)
    sbp.call(cmd, shell=True)
