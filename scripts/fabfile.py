#encoding:utf-8
from fabric.api import *
import datetime
import sys
import os

site = os.getenv('site')
if site == 'pythoner':
    env.hosts = ['t-y.me']
    env.user = 'root'
else:
    env.hosts = ['192.168.100.100']
    env.user = 'root'

def mysqldump():
    d = datetime.datetime.today()
    dbs = ['pythoner_db']
    for db in dbs:
        file_name = "%s_%s-%s-%s" %(db,d.year,d.month,d.day)
        cmd = "mysqldump -hlocalhost -uroot -p122126382 %s> /tmp/%s.sql" %(db,file_name)
        run(cmd)
        
        cmd = 'scp -C root@t-y.me:/tmp/%s.sql ~/Backup/sqls/' %file_name
        local(cmd)

def mysqlrestore():
    dbs = ['pythoner_db']
    for host in env.hosts:
        for db in dbs:
            local("scp -rC %s.sql %s@%s:~/" %(db,env.user,host))

    #with run('mysql'):
    #    run('source ~/s.sql;')

def install_base():
    run('apt-get update')
    run('apt-get  install redis-server mysql-server libxml2 git git-core automake autoconfig build-essential ')

def install_python():
    """ 
    install python2.7 
    """
    run('apt-get install python2.7 python2.7-dev')
    run('mv /usr/bin/python /usr/bin/python.bac')
    run('ln -s /usr/bin/python2.7 /usr/bin/python')
    run('apt-get install python-setuptools')
    run('easy_install-2.7 pip')
    run('mv /usr/local/bin/pip /usr/bin/pip.bac')
    run('ln -s /usr/local/bin/pip-2.7 /usr/local/bin/pip')

def install_nginx():
    # copy the config file to host
    for host in env.hosts:
        local("scp -rC nginx %s@%s:~/" %(env.user,host))
    run('add-apt-repository ppa:nginx/stable')
    run('apt-get -y install nginx')

def install_uwsgi():
    # make -f Makefile.Py26
    run('add-apt-repository ppa:uwsgi/release  ')
    run('apt-get -y install uwsgi-2.6')

def install_mysql():
    run('apt-get -y install mysql-server')
    run('apt-get install -y libmysqld-dev libmysqlclient-dev')
    for host in env.hosts:
        local("scp -rC my.cnf %s@%s:/etc/" %(env.user,host))

def restart():
    """ restart the pythoner uwsgi & nginx """
    with cd('/www/pythoner/bin'):
        run('. uwsgi')

def setup():
    install_base()
    install_python()
    install_nginx()

def deploy():
    with cd('/home/pythoner.net'):
        run('git pull origin master:master')
        run('pip install -r ~/pythoner.net/scripts/requirements.txt')
        #run('. bin/uwsgi.sh')

def run_spider():
    with cd('/www/pythoner/others/spider'):
        run('ls')
        run('. run.sh')



