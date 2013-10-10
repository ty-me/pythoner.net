# -*- coding: utf-8 -*-
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
