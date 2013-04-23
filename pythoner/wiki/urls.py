#encoding:utf-8
#CMS模块URL配置
from settings import *
from django.conf.urls.defaults import *
from feed import EntryFeed

urlpatterns = patterns(APP,
    (r'^$','views.list'),#列表页
    (r'^tag/(\S{1,10})/p(\d{1,10})/','views.tag'),#按标签查看

    (r'^p(\d{1,10})/$','views.list'),#列表翻页
    (r'^(\d{1,10})/$','views.detail'),#详细页面
    (r'^\S{1,20}/(\d{1,10})','views.detail'),

    (r'^add/(?P<method>default|markdown)/$','views.add'),#增加
    (r'^(\d{1,10})/edit/$','views.edit'),#修改
    (r'^(\d{1,10})/del/$','views.delete'),#删除
    (r'^rss.xml',EntryFeed()),

)
