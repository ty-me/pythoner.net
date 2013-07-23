#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  TY<tianyu0915@gmail.com>

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

from django.conf.urls.defaults import *

urlpatterns = patterns('pm.views',
    (r'^$','inbox'),
    (r'^inbox/$','inbox'),
    (r'^inbox/p(\d{1,10})/$','inbox'),
    (r'^outbox/$','outbox'),
    (r'^outbox/p(\d{1,10})/$','outbox'),
    (r'^write/$','write'),
    (r'delete/$','delete'),
    (r'^(\d{1,10})/','detail'),
)