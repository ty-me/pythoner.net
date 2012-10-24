# -*- coding: utf-8 -*-
# Data:11-7-16 下午4:02
# Author: T-y(master@t-y.me)
# File:urls

from django.conf.urls.defaults import *

urlpatterns = patterns('jobs.views',
    (r'^$','list'),
    (r'^p(\d){1,10}/$','list'), # 列表
    (r'^(\d{1,10})/$','detail'), # 详细页
    (r'^add/$','add'),  # 发表
)