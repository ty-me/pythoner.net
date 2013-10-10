#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

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
from feed import TopicFeed

urlpatterns = patterns('topic',
    (r'^$','views.list'), # 首页
    (r'^p(\d{1,10})/$','views.list'), # 列表
    (r'user/(\d{1,10})/$','views.list_by_user'),
    (r'user/(\d{1,10})/p(\d{1,10})/$','views.list_by_user'),
    (r'^add/$','views.add'),# 发表话题
    (r'^(\d{1,10})/$','views.detail'), # 话题详细页面
    (r'^(\d{1,10})/edit/$','views.edit'), # 编辑修话题
    (r'^(\d{1,10})/delete/$','views.delete'), # 删除话题
    (r'^/favorite/$','views.favorite'), # 用户收藏列表
    (r'^(\d{1,10})/mark/$','views.favorite_mark'), # 添加收藏
    (r'^(\S{1,20})/$','views.list_by_tag'), # 按标签查看

    (r'^rss.xml$',TopicFeed()),
)