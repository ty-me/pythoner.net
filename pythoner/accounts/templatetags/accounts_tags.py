# -*- coding: utf-8 -*-
# Data:11-6-14 下午10:09
# Author: T-y(master@t-y.me)
# File:accounts_tags
from django import template
from django.contrib.auth.models import User
from accounts.models import UserProfile


register = template.Library()

@register.inclusion_tag('account_latest.tag.html')
def get_latest_user(count=10):
    """
    得到最新注册的用户
    """

    try:
        count = int(count)
    except ValueError:
        count = 10

    users = User.objects.filter(is_active=True).order_by('-id')[0:count]
    return {'users':users}

@register.inclusion_tag('account_alive_user.tag.html')
def get_alive_user(count=200):
    """
    得到活跃用户
    """
    users = User.objects.filter(is_active=True).order_by('-last_login')[:count]
    return {'users':users}
