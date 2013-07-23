#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.NET

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
