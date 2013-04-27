# -*- coding: utf-8 -*-
# Data:11-7-27 上午12:06
# Author: TY(admin@pythoner.net)
# File:feed

from django.contrib.syndication.views import Feed
from models import Entry
import datetime
from settings import SITE_NAME
now = datetime.datetime.now()

class EntryFeed(Feed):
    title = '{0}-最近更新的文章'.format(SITE_NAME)
    link = '/feed/comment.xml'

    def items(self):
        return Entry.objects.order_by('-id').filter(public=True,sub_time__lt = now)[:15]

    def item_title(self, item):
        return u'[%s]%s -pythoner.net' %(item.category.name,item.title)

    def item_description(self, item):
        return item.content[0:40]
