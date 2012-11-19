# -*- coding: utf-8 -*-
# Data:11-7-27 上午12:06
# Author: T-y(master@t-y.me)
# File:feed
from django.contrib.syndication.views import Feed
from models import Entry
import datetime

now = datetime.datetime.now()

class EntryFeed(Feed):
    title = 'python爱好者-最近更新的文章'
    link = '/feed/comment.xml'

    def items(self):
        return Entry.objects.order_by('-id').filter(public=True,sub_time__lt = now)[:15]

    def item_title(self, item):
        return u'[%s]%s -pythoner.net' %(item.category.name,item.title)

    def item_description(self, item):
        return item.content[0:40]