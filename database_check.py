#!/usr/bin/env python
# -- coding=utf-8 --
__author__ = 'InMath'
from mysql import connector as conn
import mysql.connector.errors as mysqlerror
# import mysql.connector.errorcode as errorcode
MysqlConn = conn.connect(user="root", password="inmath", database="test", buffered=False)
sql = "show databases"
cursor = MysqlConn.cursor()
cursor.execute(sql)
databases = []
for (database,) in cursor:
    databases.append(database)

for database in databases:
    cursor.execute("use %s" % database)
    sql = "show tables"
    cursor.execute(sql)
    querys = []
    for (table,) in cursor:
        query = "select * from %s limit 1" % table
        querys.append(query)
    for query in querys:
        try:
            cursor.execute(query)
            cursor.fetchall()
        except mysqlerror.Error as error:
            print error
            exit(0)




