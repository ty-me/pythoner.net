#encoding:utf-8

# -*- coding: utf-8 -*-
# Data:10-7-20 下午6:54
# Author: T-y(master@t-y.me)
# File:main_tags

from django.contrib.comments.models import Comment
from django.template import Library

register = Library()

@register.inclusion_tag('latest_comment.tag.html')
def get_latest_comment(count=6):
    comments = Comment.objects.order_by('-id')[0:count]
    return {'comments':comments}

