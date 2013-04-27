# -*- coding: utf-8 -*-
# Data:11-7-27 上午12:04
# Author: T-y(master@t-y.me)
# File:feed
from django.contrib.syndication.views import Feed
from topic.models import Topic
from settings import SITE_NAME

class TopicFeed(Feed):
    title = '{0}最新话题'.format(SITE_NAME)
    link = '/feed/topic.xml'

    def items(self):
        return Topic.objects.order_by('-id').filter(deleted=False)[0:10]

    def item_title(self, item):
        return item.title + '-pythoner.net'

    def item_description(self, item):
        return item.content[:20]
