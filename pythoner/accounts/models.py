#encoding:utf-8
from django.contrib.auth.models import User
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save

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

class Link(models.Model):
    user = models.ForeignKey(User)
    type= models.CharField('类型',max_length=10)
    name = models.CharField('链接名称',max_length=20)
    url = models.URLField('链接')

    def __unicode__(self):
        return self.link

