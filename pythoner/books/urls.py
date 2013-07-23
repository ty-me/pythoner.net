#encoding:utf-8
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

#CMS模块URL配置
from settings import *
from django.conf.urls.defaults import *


urlpatterns = patterns('books',
    (r'^$','views.list'),#列表页
    (r'^p(\d{1,10})/$','views.list'),#列表翻页
    (r'^(\d{10,14})/$','views.detail'),#详细页面
    (r'^add/$','views.add'),#增加
    (r'^(\d{1,10})/edit/$','views.edit'),#修改
    (r'^(\d{1,10})/del/$','views.delete'),#删除
    (r'^(\S{1,20})/','views.category'),#按分类查看

)
