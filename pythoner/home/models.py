#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from code.models import Base
from topic.models import Topic
from home.signals import photo_was_uploaded
import datetime
import time
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from topic.signals import new_topic_was_posted
from code.signals import new_code_was_post
from wiki.signals import new_wiki_was_post
from django.db.models.signals import post_save

class UserRlation(models.Model):
    """
    用户关系表 type:friend,black
    """
    source_user = models.ForeignKey(User,verbose_name='用户A',related_name='user_a')
    target_user = models.ForeignKey(User,verbose_name='用户B',related_name='user_b')
    type = models.CharField('关系类型',max_length=15,default='friend')

    def __unicode__(self):
        return u'%s %s [%s]' %(self.source_user,self.target_user,self.type)

    class Meta:
        verbose_name_plural = '用户关系'

class Type(models.Model):
    """
    动态类型
    """
    name = models.CharField('类型',max_length=50)

    def __unicode__(self):
        return self.name 

    class Meta:
        verbose_name_plural = '动态类型'

class Develop(models.Model):
    """
    动态
    """
    user = models.ForeignKey(User,verbose_name='用户',related_name='user')
    type = models.ForeignKey(Type,verbose_name='动态类型',related_name='type')
    sub_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'[%s]-%s' %(self.type,self.user.get_profile().screen_name)

    class Meta:
        ordering = ['-sub_time']
        verbose_name_plural = '用户动态'

class Object(models.Model):
    """
    动态对象
    """
    develop = models.ForeignKey(Develop)
    object_id = models.PositiveIntegerField('对象ID',max_length=10)

    def __unicode__(self):
        return u'%s - %d' %(self.develop, self.object_id)

    class Meta:
        verbose_name_plural = '动态对象'

class Visitor(models.Model):
    """
    来访者
    """
    master = models.ForeignKey(User,verbose_name='主人',related_name='master')
    visitor = models.ForeignKey(User,verbose_name='访客',related_name='visitor')
    sub_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-sub_time']
        verbose_name_plural = '来访者'

    def __unicode__(self):
        return u'%s <- %s' %(self.master.get_profile().screen_name,self.visitor.get_profile().screen_name)

############################################# 华丽的分割线 #############################################

def comment_develop(sender,instance,**kwargs):
    user = instance.user
    # 游客则跳过
    if not user:
        return
    try:
        content_type = ContentType.objects.get(id=instance.content_type.id)
    except ContentType.DoesNotExist,e:
        return
    type,type_created = Type.objects.get_or_create(name='%s_comment' %content_type.app_label)

    obj_exist = False
    objects = Object.objects.filter(object_id=instance.object_pk) # 找到所有可能的对象
    for obj in objects:
        if obj.develop.type == type:
            develop,obj_exist = obj.develop,True # 改对象存在
            break

    if obj_exist:
        develop.save() # 更新改动态时间戳
    else:
        develop = Develop(user=user,type=type)
        develop.save()
        Object(develop=develop,object_id=instance.object_pk).save()

def topic_develop(sender,**kwargs):
    topic = kwargs['topic']
    type,type_created = Type.objects.get_or_create(name='topic')
    user = topic.author

    # 找到一天以内的动态，如果没有则创建一个
    yesterday = datetime.datetime.fromtimestamp(time.time()-2600*24)
    develop_all = Develop.objects.filter(user=user,type=type,sub_time__gt=yesterday)
    if develop_all.count() == 0:
        develop = Develop(user=user,type=type)
        develop.save()
    else:
        develop = develop_all[0]
        develop.save() # 更新时间

    Object.objects.get_or_create(develop=develop,object_id=topic.id)

def photo_develop(sender,**kwargs):
    """
    用户更新头像动态
    """
    type,type_created = Type.objects.get_or_create(name='photo')
    user = kwargs['user']
    develop,created = Develop.objects.get_or_create(user=user,type=type)
    develop.sub_time = datetime.datetime.now()
    develop.save()

def relation_develop(sender,instance,**kwargs):
    """
    用户关系动态
    """
    if instance.type <> 'friend':
        return

    # 取出参数
    target_user = instance.target_user
    type,type_created = Type.objects.get_or_create(name='relation')
    user = instance.source_user

    # 找到一天以内的动态，如果没有则创建一个
    yesterday = datetime.datetime.fromtimestamp(time.time()-2600*24)
    develop_all = Develop.objects.filter(user=user,type=type,sub_time__gt=yesterday)
    if develop_all.count() == 0:
        develop = Develop(user=user,type=type,sub_time=datetime.datetime.now())
        develop.save()
    else:
        develop = develop_all[0]
        develop.save() # 更新时间
    Object.objects.get_or_create(develop=develop,object_id=target_user.id)

def code_develop(sender,**kwargs):
    """
    发布代码动态
    """
    code = kwargs['code']
    type,type_created = Type.objects.get_or_create(name='code')
    user = code.author

    # 找到一天以内的动态，如果没有则创建一个
    yesterday = datetime.datetime.fromtimestamp(time.time()-3600*24)
    develop_all = Develop.objects.filter(user=user,type=type,sub_time__gt=yesterday)
    if develop_all.count() == 0:
        develop = Develop(user=user,type=type)
        develop.save()
    else:
        develop = develop_all[0]
        develop.save() # 更新时间
    Object.objects.get_or_create(develop=develop,object_id=code.id)


def wiki_develop(sender,**kwargs):
    """
    发表笔记动态
    """
    wiki = kwargs['wiki']
    type,type_created = Type.objects.get_or_create(name='wiki')
    user = wiki.author

    # 找到一天以内的动态，如果没有，则创建一个新的动态
    yesterday = datetime.datetime.fromtimestamp(time.time()-3600*24)
    develop_all = Develop.objects.filter(user=user,type=type,sub_time__gt=yesterday)
    if develop_all.count() ==0:
        develop = Develop(user=user,type=type)
        develop.save()
    else:
        develop = develop_all[0]
        develop.save()  # 保存一下，更新这个动态的最新时间
    Object.objects.get_or_create(develop=develop,object_id=wiki.id) # 为这个动态添加对象


new_topic_was_posted.connect(topic_develop)
photo_was_uploaded.connect(photo_develop)
post_save.connect(comment_develop,sender=Comment)
post_save.connect(relation_develop,sender=UserRlation)
new_code_was_post.connect(code_develop)
new_wiki_was_post.connect(wiki_develop)

