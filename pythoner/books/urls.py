#encoding:utf-8
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
