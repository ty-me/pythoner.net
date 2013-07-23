#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.NET

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

from django import template
from topic.models import Topic,Favorite,Tag
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('topic_latest.tag.html')
def get_latest_topic(count=10):
    """
    得到最新的话题
    """
    topics = Topic.objects.order_by('-sub_time')[0:count]
    return {'entrys':topics}

@register.inclusion_tag('topic_list_by_user.tag.html')
def get_topic_list_by_user(user,count=10):
    """
    用户发起的话题
    """
    return {'topics':Topic.objects.filter(author=user,deleted=False)[0:count],
            'user':user}

@register.inclusion_tag('topic_mark_list.tag.html')
def get_user_favorite(user_id):
    """
    获取用户的收藏
    """
    try:
        user_id = int(user_id)
        user = User.objects.get(id=user_id)
    except (ValueError,User.DoesNotExist):
        pass

    favorites = Favorite.objects.filter(user=user)[0:5]
    return {'entrys':favorites,'title':'收藏的'}

@register.filter
def mark(user,topic):
    """
    返回用户是否标记
    """
    count = Favorite.objects.filter(topic=topic).count()

    try:
        Favorite.objects.get(user=user,topic=topic)
    except Favorite.DoesNotExist:
        result = '+ Mark'
    else:
        result = 'Marked'

    return result

@register.filter
def click_count(count):
    if count <= 999:
        return count
    return str(count/1000)+'k'

@register.inclusion_tag('topic_tag.tag.html')
def get_topic_tag():
    return {'tags': Tag.objects.all()}