#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('main',
    # custom api
    ('^api/wiki/add/','wiki_api.add'),
    ('^api/wiki/edit/','wiki_api.edit'),

    ('^verify/','views.verify_code'),
    #('^oh-my-god/','views.verify'),
    ('^random/$','views.random'),
    ('^emailrss/','views.email_rss'),
    (r'^usernav/$','views.usernav'),
)
