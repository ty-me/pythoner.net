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
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from accounts.signals import update_user_repulation
from django.contrib import messages
from utils.logger import getlogger
log = getlogger(__name__)

class UserProfile(models.Model):
    """
    用户资料 pythoner_net
    """
    user = models.ForeignKey(User,unique=True)
    screen_name = models.CharField('昵称',max_length=10,blank=False,null=False,help_text='长度为1~10个字符')
    score = models.PositiveIntegerField('积分',max_length=5,default=0)
    deleted = models.BooleanField('删除',default=False)
    
    photo = models.ImageField('头像',upload_to='user',blank=True)
    city = models.CharField('城市',max_length=15,default='北京')
    status = models.CharField('签名',max_length=150,blank=True,help_text='设置你的签名，最大长度为150字符')
    introduction = models.CharField('介绍',max_length=200,blank=True,help_text='个人介绍最大长度为200字符')
    #signup_from = models.CharField('signup from',max_length=30,default='pythoner')

    def __unicode__(self):
        return self.screen_name

class Repulation(models.Model):
    """
    用户声望记录
    """

    user            = models.ForeignKey(User)
    action          = models.CharField('操作',max_length=20)
    content_type    = models.CharField('类型',max_length=20)
    count           = models.IntegerField('数量')
    url             = models.URLField('链接')
    title           = models.CharField('标题',max_length=500)
    created_at      = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return u'[{}]{}-{}'.format(self.content_type,self.title,self.count)

class Link(models.Model):
    user = models.ForeignKey(User)
    type= models.CharField('类型',max_length=10)
    name = models.CharField('链接名称',max_length=20)
    url = models.URLField('链接')

    def __unicode__(self):
        return self.link

def _update_user_repulation(sender,**kwargs):
    """   处理用户声望更新的信号

    """
    try:
        user        = kwargs['user']
        request     = kwargs['request']
        profile     = user.get_profile()
        action      = kwargs['action']
        title       = kwargs['title']
        message     = kwargs['message']
        url         = kwargs['url']
        content_type = kwargs['content_type']
        score_dict = {
                'add_wiki':15,
                'add_topic':15,
                'add_link':5,
                'delete_wiki':-15,
                'delete_topic':-10,
        }
        key = '{}_{}'.format(action,content_type)
        count = score_dict.get(key)

        if not count:
            return False

        profile.score += count
        profile.save()
        repulation = Repulation(user=user,content_type=content_type,title=title,url=url,action=action,count=count)
        repulation.save()
        
        # 如果是用户自己的行为使得声望增加，则显示messages提示声望值的变化情况，
        # 否则发送pm通知提示
        if request.user and request.user.id == user.id:
            message = u'{},声望{}{}'.format(message,count>=0 and '+' or '',count)
            messages.success(request,message)
        return True

    except Exception,e:
        log.error(e)
        return False

update_user_repulation.connect(_update_user_repulation)
