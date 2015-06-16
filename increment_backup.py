#!/usr/bin/env python
# -- coding=utf-8 --
__author__ = 'InMath'
import subprocess as sbp
import time as tm
import os
import sys

from BackupUtil import iniconfigparser


cp = iniconfigparser("database.ini")
now = tm.strftime("%Y%m%d%H%M%S", tm.localtime(int(tm.time())))
# print now
dbuser = cp.get("database", "user")  # 数据库用户名
dbpass = cp.get("database", "password")  # 数据库密码
sockpath = cp.get("database", "socketpath")  # socket文件路径
increment_root_path = cp.get("backup", "increment_root_path")  # 增量备份存储路径
full_root_path = cp.get("back", "full_root_path")  # 全备文件目录
increment_base_dir = ""  # 增量备份基础文件目录
increment_store_dir = ""  # 增量备份存储文件目录
full_backup_path = ""  # 全备文件目录
cmd = "innobackupex --user=%s " \
      "--password=%s --socket=%s --no-timestamp " \
      "--incremental %s --incremental-basedir=%s"  # 增量备份shell命令
if not os.path.exists(increment_root_path):
    os.makedirs(increment_root_path)
if not os.path.exists(full_root_path):
    os.makedirs(full_root_path)
# 寻找最新的全备目录
tmp = 0
for filepath in os.listdir(full_root_path):
    if os.path.isdir(full_root_path + "/" + filepath) and tmp < int(filepath):
        tmp = int(filepath)
if tmp == 0 or (len(sys.argv) > 1 and sys.argv[1] == 'fullbackup'):
    # 全量备份不存在，执行一次全量备份
    # 或传入参数fullbackup,进行强制全量备份，并退出程序
    full_backup_path = full_root_path + '/' + now
    cmd = "innobackupex --defaults-file=/etc/my.cnf " \
          "--user=%s --password=%s --socket=%s  " \
          "--no-timestamp %s" % (dbuser, dbpass, sockpath, full_backup_path)
    sbp.call(cmd, shell=True)
    exit(0)
full_backup_path = full_root_path + '/' + str(tmp)

# 验证全备对应的增备目录是否存在
increment_store_path = increment_root_path + '/base_' + str(tmp)
if not os.path.exists(increment_store_path):
    os.makedirs(increment_store_path)
    increment_base_dir = full_backup_path
    increment_store_dir = increment_store_path + '/' + now

    # 执行基于全备文件的首次增量备份，并退出程序
    cmd = cmd % (dbuser, dbpass, sockpath, increment_store_dir, increment_base_dir)
    sbp.call(cmd, shell=True)
    exit(0)
else:
    # 如果增量目录存在，就执行基于已有增量为基准的增量备份
    # 寻找最新增量备份目录
    tmp = 0
    for filepath in os.listdir(increment_store_path):
        if os.path.isdir(increment_store_path + '/' + filepath) and tmp < int(filepath):
            tmp = int(filepath)
    increment_base_dir = increment_store_path + '/' + str(tmp)
    increment_store_dir = increment_store_path + '/' + now
    cmd = cmd % (dbuser, dbpass, sockpath, increment_store_dir, increment_base_dir)

    #  执行增量备份命令
    sbp.call(cmd, shell=True)
    exit(0)





