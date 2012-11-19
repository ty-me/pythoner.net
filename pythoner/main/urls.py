#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('main',
    ('^verify/','verify.views.display'),
    ('^random/$','views.random'),
    ('^emailrss/','views.email_rss'),
    (r'^usernav/$','views.usernav'),
)
