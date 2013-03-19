#encoding:utf-8
import datetime
import sys
import os
from fabric.api import *
from cuisine import *
from fabric.contrib.project import rsync_project, upload_project
from fabric.operations import get,put
from fabric.contrib.files import  exists

env.hosts = ['192.168.2.147']
env.user = 'root'
path = '/home/pythoner.net'

def mysqldump():
    d = datetime.datetime.today()
    dbs = ['pythoner_db']
    for db in dbs:
        file_name = "%s_%s-%s-%s" %(db,d.year,d.month,d.day)
        cmd = "mysqldump -hlocalhost -uroot  %s> /tmp/%s.sql" %(db,file_name)
        run(cmd)
        
        get('/tmp/%s.sql' %file_name,'~/Sqls/')

def mysqlrestore():
    dbs = ['pythoner_db']
    for host in env.hosts:
        for db in dbs:
            local("scp -rC %s.sql %s@%s:~/" %(db,env.user,host))

    #with run('mysql'):
    #    run('source ~/s.sql;')

def restart():
    """ restart the pythoner uwsgi & nginx """
    run('nginx -s reload')
    with cd(path):
        with cd('scripts'):
            run('sh uwsgi.sh')

def sync_code():
    if not exists(path):
        with cd('/home/'):
            run('git clone https://github.com/tianyu0915/pythoner.net.git')

    with cd(path):
        run('git checkout -- .')
        run('git pull origin master')

def setup():
    # env 
    if not exists('/www/pythoner'):
        run('mkdir /www/')
        with cd('/www/'):
            run('ln -s /home/pythoner.net/pythoner .')

    with cd(path):
        with cd('scripts'):
            run('source setupenv.sh')

    # config
    put('config/pythoner','/etc/nginx/conf.d/pythoner')

def deploy():
    sync_code()
    setup()
    restart()

def run_spider():
    with cd('/www/pythoner/others/spider'):
        run('ls')
        run('. run.sh')


