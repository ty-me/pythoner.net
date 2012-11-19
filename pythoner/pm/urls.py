#encoding:utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('pm.views',
    (r'^$','inbox'),
    (r'^inbox/$','inbox'),
    (r'^inbox/p(\d{1,10})/$','inbox'),
    (r'^outbox/$','outbox'),
    (r'^outbox/p(\d{1,10})/$','outbox'),
    (r'^write/$','write'),
    (r'delete/$','delete'),
    (r'^(\d{1,10})/','detail'),
)