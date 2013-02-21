#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('main',
    ('^verify/','views.verify_code'),
    ('^random/$','views.random'),
    ('^emailrss/','views.email_rss'),
    (r'^usernav/$','views.usernav'),
)
