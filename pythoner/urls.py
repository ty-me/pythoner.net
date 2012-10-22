#encoding:utf-8
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from main.feeds import *
from django.views.decorators.cache import cache_page

admin.autodiscover()

urlpatterns = patterns('',
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
    (r'^search/',include('search.urls')),
    (r'^members/$','home.views.members'),

    (r'^main/',include('main.urls')),
    (r'^(\S{1,10})/$','main.views.plink'),
)
