#encoding:utf-8
import os,sys
import gevent
from gevent import monkey
from gevent import wsgi
from gevent import socket


import pwd
#pe = pwd.getpwnam("www-data")
monkey.patch_all()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

sys.path.insert(0,'/www/')
sys.path.insert(0,'/www/pythoner')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pythoner.settings'

try:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
except:
    host = 'pythoner.net'
    port = 80
finally:
    print 'runing at %s:%s' %(host,port)

server = wsgi.WSGIServer((host,port),application)
server.serve_forever()
