#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

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
from django.conf import settings
from django.contrib import admin
from main.feeds import *
from django.views.decorators.cache import cache_page

admin.autodiscover()

urlpatterns = patterns('',
    (r'^upload/$','main.upload.general_file_upload_handle'),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    (r'^favicon.ico$','django.views.generic.simple.redirect_to',{'url':'/static/images/favicon.ico'}),
    (r'^comments/',include('django.contrib.comments.urls')),
    (r'^admin/',include(admin.site.urls)),
    (r'^$','main.views.index'),
    (r'^link/',include('link.urls')),
    (r'jobs/',include('jobs.urls')),
    (r'^topic/',include('topic.urls')),
    (r'^wiki/',include('wiki.urls')),
    (r'^home/',include('home.urls')),
    (r'^pm/',include('pm.urls')),
    (r'^code/',include('code.urls')),
    (r'^books/',include('books.urls')),
    (r'^accounts/',include('accounts.urls')),
    (r'^members/$','home.views.members'),


    (r'^main/',include('main.urls')),
    (r'^(\S{1,10})/$','main.views.plink'),
    (r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
