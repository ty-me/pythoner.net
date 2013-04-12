#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('main',
    ('^api/wiki/add/','wiki_api.add'),
    ('^verify/','views.verify_code'),
    ('^random/$','views.random'),
    ('^emailrss/','views.email_rss'),
    (r'^usernav/$','views.usernav'),
)
