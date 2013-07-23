# -*- coding: utf-8 -*-
"""
pythoner.net
Copyright (C) 2013  TY<tianyu0915@gmail.com>

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
from models import Entry
import datetime
from pythoner.settings import SITE_NAME
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
