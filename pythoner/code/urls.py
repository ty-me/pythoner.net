# -*- coding: utf-8 -*-
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
