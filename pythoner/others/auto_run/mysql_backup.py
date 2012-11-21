#!/usr/bin/python
#encoding:utf-8
import os
import sys
import time

"""
mysql 自动备份脚本
"""

# 配置信息
db_user = 'root'
db_name = 'pythoner_db'
db_password = '123456'
backup_to =  os.path.join(os.path.normpath(os.path.dirname(__file__)),'..','database_backup')

today = time.strftime('%Y-%m-%d-%H%M')
file_name = '%s.%s.sql' %(today,db_name)
file_path = os.path.join(backup_to,file_name)

# 创建目录
if not os.path.exists(backup_to):
    os.mkdir(backup_to)

# 构造命令

cmd = " mysqldump -u%s -p%s %s > %s" %(db_user,db_password,db_name,file_path)
os.system(cmd)
print '%s- cmd:%s' %(today,cmd)

