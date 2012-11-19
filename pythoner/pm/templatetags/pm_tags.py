# -*- coding: utf-8 -*-
# Data:11-6-14 下午5:49
# Author: T-y(master@t-y.me)
# File:pm_tags.py
# 热死哥哥我了啊~~~！
from django import template
from pm.models import Pm

register = template.Library()

# 统计未读PM数量
@register.filter
def pm_count(user):
    count = Pm.objects.filter(to_user=user,to_deleted=False,readed=False).count()
    return count <> 0 and "(<span class=\"red\">%d</span>)" %count or ''