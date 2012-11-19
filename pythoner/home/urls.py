#encoding:utf-8
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
    (r'^members/p(\d{1,10})/$','views.members') # 成员
)
