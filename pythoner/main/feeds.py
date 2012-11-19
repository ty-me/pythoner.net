# -*- coding: utf-8 -*-
# Data:11-7-20 下午5:08
# Author: T-y(master@t-y.me)
# File:feed
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