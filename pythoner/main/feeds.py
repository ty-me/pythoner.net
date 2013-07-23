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
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

class CommentFeed(Feed):
    title = '最新评论'
    link = '/feed/comment.xml'

    def items(self):
        return Comment.objects.order_by('-id')[:15]

    def item_title(self, item):
        if item.user_id:
            return User.objects.get(id=item.user_id).get_profile().screen_name+' :%s' %item.comment
        else:
            return '%s :%s' %(item.user_name,item.comment)

    def item_description(self, item):
        return item.comment