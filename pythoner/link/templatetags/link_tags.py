# -*- coding: utf-8 -*-
# Data:11-7-13 下午8:03
# Author: T-y(master@t-y.me)
# File:link_tags
from django import template
from link.models import *

register = template.Library()

@register.inclusion_tag('link_list.tag.html')
def get_link_by_category(category_id=1):
    try:
        category_id = int(category_id)
    except :
        category_id = 1
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        category = Category.objects.get(id=1)
    links = Link.objects.order_by('id').filter(display=True,category=category)
    if links.count()>0:
        return {'title':category.name,'links':links}
    else:
        pass