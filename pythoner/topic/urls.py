#encoding:utf-8
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