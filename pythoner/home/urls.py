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

from django.conf.urls.defaults import *

urlpatterns = patterns('home',
    (r'^$','views.index'), # 已登录用户首页
    (r'^p(\d{1,10})/$','views.index'), # 用户首页(翻页)
    (r'^(\d{1,10})/$','profile.index'),# 用户档案
    (r'^(\d{1,10})/p(\d{1,10})/$','profile.index'),# 用户档案(翻页)
    (r'^(\d{1,10})/follow/$','relation.follow'), # 关注用户
    (r'^(\d{1,10})/follows/$','relation.follows'), # 用户关注的对象
    (r'^(\d{1,10})/fans/$','relation.fans'), # 用户关的粉丝

    (r'^(\d{1,10})/code/$','views.code'), # 用户发布的代码
    (r'^(\d{1,10})/code/p(\d{1,10})/$','views.code'), # 用户发布的代码(翻页)

    (r'^(\d{1,10})/topic/$','views.topic'), # 用户发起的话题
    (r'^(\d{1,10})/topic/p(\d{1,10})/$','views.topic'), # 用户发起得话题(翻页

    (r'^(\d{1,10})/wiki/','userwiki.list'), # 用户板报列表

    (r'^edit/$','profile.edit'), # 编辑用户档案
    (r'^delete/$','profile.delete'), # 删除账号
    (r'^password/$','profile.password'), # 修改密码
    (r'^photo/$','profile.photo'), # 修改头像
    (r'^link/$','profile.link'),
    (r'^city/$','city.index'), # 城市列表
    (r'^members/$','views.members'), # 成员
    (r'^members/p(\d{1,10})/$','views.members'), # 成员
)
