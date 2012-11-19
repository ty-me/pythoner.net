#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('accounts',
    ('^login/$','views.login'),

    ('^login/sina/$','sina.index'),
    (r'login/sina/callback/$','sina.callback'),

    #('^login/douban/$','douban.index'),
    #(r'login/douban/callback/$','douban.callback'),

    #('^login/twitter/$','twitter.index'),
    #(r'login/twitter/callback/$','twitter.callback'),

    ('^logout/$','views.logout'),
    ('^register/$','views.register'),
    (r'^active/(\d{1,10})/(.*)/$','views.active'),

)
