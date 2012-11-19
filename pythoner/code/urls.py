# -*- coding: utf-8 -*-
# Data:11-7-25 上午10:25
# Author: T-y(master@t-y.me)
# File:urls
from django.conf.urls.defaults import *

urlpatterns = patterns('code.views',
    ('^$','list'), # 列表
    (r'^p(\d{1,10})/$','list'), # 列表（分页）
    (r'user/(\d{1,10})/$','list_by_user'), # 安用户查看
    (r'user/(\d{1,10})/p(\d{1,10})/$','list_by_user'), # 安用户查看
    (r'^add/$','add'),

    (r'^(\d{1,10})/$','detail'), # 详细

    (r'add/(\d{1,10})/$','add_by_paste'), # 上传/粘贴代码
    (r'add/(\d{1,10})/paste/$','add_by_paste'), # 粘贴代码
    (r'add/(\d{1,10})/file/$','add_by_file'), # 上传文件

    (r'(\d{1,10})/del/(\d{1,10})/$','del_code'), # 删除已有代码
    (r'(\d{1,10})/edit/(\d{1,10})/$','edi_code'), # 修改已有代码
    (r'add/(\d{1,10})/publish/$','publish'), # 发布代码

    (r'^download/(\S{1,10})/(\d{1,10})/$','download'), # 下载附件

    (r'^add/(\d{1,10})/file/$','add_by_file'),# 添加代码
    (r'^del/(\d{1,10})/$','delete'), # 删除代码

)
