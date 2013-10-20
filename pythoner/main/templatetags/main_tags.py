#encoding:utf-8
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

import re
from django.contrib.comments.models import Comment
from django.template import Library

register = Library()

@register.inclusion_tag('latest_comment.tag.html')
def get_latest_comment(count=6):
    comments = Comment.objects.order_by('-id')[0:count]
    res = []
    for c in comments:
        li = {}
        li['comment'] =  re.compile(r'<[^>]+>',re.S).sub('',c.comment)
        li['url']     = c.get_absolute_url()
        res.append(li)
    return {'comments':res}

@register.inclusion_tag('sidebar_ads.tag.html')
def render_sidebar_ads():
    return ''


