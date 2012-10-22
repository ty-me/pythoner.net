# -*- coding: utf-8 -*-
# Data:11-7-3 上午12:33
# Author: T-y(master@t-y.me)
# File:url
from django.conf.urls.defaults import *

urlpatterns = patterns('link',
    (r'^$','views.index'),
    (r'^add/$','views.add'),
    (r'posted/$','views.posted'),
)