# -*- coding: utf-8 -*-
# Data:11-8-2 上午10:43
# Author: T-y(master@t-y.me)
# File:code_tags
from django.template import Library
from code.models import *

register = Library()

@register.inclusion_tag('code_list_by_user.tag.html')
def get_code_list_by_user(user,count=10):
    """
    得到用户分享的代码
    """
    return {'codes':Base.objects.filter(author=user,display=True)[0:count],
            'user':user}

@register.inclusion_tag('code_category.tag.html')
def get_code_category():
    """
    得到代码分类
    """
    return {'categorys':Category.objects.all()}

@register.inclusion_tag('code_visitor.tag.html')
def get_code_visitor(base,count=90):
    """
    阅读过该代码的访客
    """
    return {'visitors':Visitor.objects.filter(base=base).order_by('-sub_time')[0:count],'count':count}

@register.inclusion_tag('code_latest.tag.html')
def get_latest_code(count=10):
    """
    得到最新的代码
    """
    return {'codes':Base.objects.filter(display=True)[:count]}

@register.inclusion_tag('code_click.tag.html')
def get_code_by_clicktime(count=10):
    """
    得到点击最多的代码列表
    """
    return {'codes':Base.objects.filter(display=True).order_by('-click_times')[:15]}
