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
from wiki.models import *
import datetime

register = template.Library()
nowtime = datetime.datetime.now()

#获取分类
@register.inclusion_tag('wiki_category.tag.html')
def get_wiki_category():
    try:
        category_list = Category.objects.all()
    except Category.DoesNotExist:
        category_list = ''
    return {'category_list':category_list}

#获取点击排行
@register.inclusion_tag('wiki_click.tag.html')
def get_wiki_by_clicktime(count=10):
    try:
        entry_list = Entry.objects.filter(sub_time__lt = nowtime,public=True).order_by('-click_time')[0:count]
    except Entry.DoesNotExist:
        entry_list = ''
    return {'entry_list':entry_list}

#获取标签列表
@register.inclusion_tag('wiki_tag.tag.html')
def get_wiki_tag(count=30):
    return {'tags':Tag.objects.all()[0:count]}

# 获取最新
@register.inclusion_tag('wiki_latest.tag.html')
def get_latest_wiki(count=10):
    entrys = Entry.objects.filter(sub_time__lt = nowtime,public=True)[0:count]
    return {'entrys':entrys}

@register.inclusion_tag('wiki_article.tag.html')
def get_wiki_article(count):
    wikis = Entry.objects.order_by('-id').filter(sub_time__lt = nowtime)[:count]
    return {'wikis':wikis}

