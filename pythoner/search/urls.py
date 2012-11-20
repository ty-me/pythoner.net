#encoding:utf-8
#CMS模块URL配置
from settings import *
from django.conf.urls.defaults import *

urlpatterns = patterns('search',
    (r'autocomplete/$','views.autocomplete'),
    (r'^(\S{1,10})/p(\d{1,10})/','views.search'),#列表页

)
