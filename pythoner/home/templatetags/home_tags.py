# -*- coding: utf-8 -*-
# Data:11-8-4 下午11:07
# Author: T-y(master@t-y.me)
# File:home_tags
from django.template import Library
from home.models import *
from wiki.models import Entry
import datetime

register = Library()

@register.inclusion_tag('develop_topic.tag.html')
def get_topic_develop(develop):
    """
    发表话题动态
    """
    objects = Object.objects.filter(develop=develop)
    id_list = [object.object_id for object in objects]
    return {'topics':Topic.objects.filter(id__in=id_list)}

@register.inclusion_tag('develop_topic_comment.tag.html')
def get_topic_comment_develop(develop):
    """
    回复话题动态
    """
    objects = Object.objects.filter(develop=develop)
    id_list = [object.object_id for object in objects]
    return {'topics':Topic.objects.filter(id__in=id_list)}

@register.inclusion_tag('develop_photo.tag.html')
def get_photo_develop(develop):
    """
    更新头像动态
    """
    return {'user':develop.user}

@register.inclusion_tag('develop_code.tag.html')
def get_code_develop(develop):
    """
    用户分享代码动态
    """
    objects = Object.objects.filter(develop=develop)
    id_list = [int(object.object_id) for object in objects]
    return {'codes':Base.objects.filter(id__in=id_list)}


@register.inclusion_tag('develop_wiki.tag.html')
def get_wiki_develop(develop):
    """
    用户分享笔记动态
    """
    objects = Object.objects.filter(develop=develop)
    id_list = [int(object.object_id) for object in objects]
    return {'wikis':Entry.objects.filter(id__in=id_list)}

@register.inclusion_tag('develop_code_comment.tag.html')
def get_code_comment_develop(develop):
    """
    解些代码评论动态
    """
    objects = Object.objects.filter(develop=develop)
    id_list = [int(object.object_id) for object in objects]
    return {'codes':Base.objects.filter(id__in=id_list)}

@register.inclusion_tag('develop_wiki_comment.tag.html')
def get_wiki_comment_develop(develop):
    objects = Object.objects.filter(develop=develop).order_by('object_id')
    id_list = [int(object.object_id) for object in objects]
    return {'wikis':Entry.objects.filter(id__in=id_list)}

@register.inclusion_tag('develop_relation.tag.html')
def get_relation_develop(develop):
    """
    用户关系动态
    """
    objects = Object.objects.filter(develop=develop)
    id_list = [int(object.object_id) for object in objects]
    return {'users':User.objects.filter(id__in=id_list)}

@register.inclusion_tag('develop_user_status.tag.html')
def get_user_status_develop(develop):
    """
    用户更新头像动态
    """
    object = Object.objects.get(develop)
    try:
        user = User.objects.get(id=object.object_id)
    except User.DoesNotExist:
        user = User.objects.get(id=1)
    return {'user':user}

@register.filter()
def how_long(sub_time):
    import time
    try:
        now_time = time.time()
        sub_time = time.mktime(sub_time.utctimetuple()) #将转换为秒
    except TypeError:
        sub_time = time.mktime(datetime.datetime.now())
    except Exception,e:
        return sub_time
    s = int(now_time - sub_time)
    #1分钟以内
    if s<=60:
        result = s,'秒'
    #1小时以内
    elif s<=60*60:
        result = s//60,'分钟'
    #1天以内
    elif s<=60*60*24:
        result = s//(60*60),'小时'
    #31天以内
    elif s<=60*60*24*31:
        result = s//(60*60*24),'天'
    #1年以内
    elif s<=60*60*24*365:
        result = s//(60*60*24*31),'月'
    else:
        result = s//(60*60*24*365),'年'

    return str(result[0])+result[1]+'前'

@register.filter
def get_relation(source_user,target_user):
    """
    得到用户关系
    """
    if source_user.is_anonymous():
        return '关注此人'

    try:
        ship = UserRlation.objects.get(source_user=source_user,target_user=target_user)
    except UserRlation.DoesNotExist:
        return '关注此人'
    if ship.type == 'friend':
        return '已关注'
    elif ship.type == 'black':
        return '已加黑'

@register.inclusion_tag('home_friends.tag.html')
def get_user_friends(user,count=30):
    """
    得到用户关注、粉丝
    """
    return {'follows':UserRlation.objects.filter(source_user=user)[0:count],
            'fans':UserRlation.objects.filter(target_user=user)[0:count],
            'user':user}

@register.inclusion_tag('home_visitor.tag.html')
def get_home_visitor(master,count=30):
    """

    """
    return {'visitors':Visitor.objects.filter(master=master).order_by('-sub_time'),'count':count}
