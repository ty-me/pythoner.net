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

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from accounts.signals import new_user_register
from settings import DOMAIN

# 与其它模块耦合,用于其他项目时不需导入这些
from topic.models import Topic
from code.models import Base
from wiki.models import Entry
from jobs.signals import new_job_was_post

class Pm(models.Model):
    """
    用户个人消息模块
    """
    from_user = models.ForeignKey(User,verbose_name='发件人',related_name='from_user')
    to_user = models.ForeignKey(User,verbose_name='收件人',related_name='to_user')
    title = models.CharField('标题',max_length=150)
    content = models.TextField('内容')
    sub_time = models.DateTimeField('时间',auto_now_add=True)

    from_deleted = models.BooleanField('发送者删除标志',default=False)
    to_deleted = models.BooleanField('接收者删除标志',default=False)
    readed = models.BooleanField('已读标志',default=False)
    system = models.BooleanField('系统邮件',default=False)

    class Meta:
        ordering = ['readed','-sub_time',] 
        verbose_name_plural = '用户短信' 

    def __unicode__(self):
        return u'%s -->%s: %s' %(self.from_user.get_profile().screen_name,self.to_user.get_profile().screen_name,self.sub_time)

def comment_notice(sender,instance,**kwargs):
    """
    当用户发表的内容有新回复是，通过PM通知用户
    """
    print 'instance',dir(instance)
    instance.comment = 'abcd'
    try:
        content_type = ContentType.objects.get(id=instance.content_type.id)
    except ContentType.DoesNotExist:
        return
    funcs = {
        'topic':_topic_notice,
        'code':_code_notice,
        'wiki':_wiki_notice,
        'jobs':do_nothing,
        'books':do_nothing,
    }
    app_label = content_type.app_label
    if app_label:

        try:
            res =  funcs[app_label](instance)
        except Exception:
            return False
        else:
            return res

def _topic_notice(comment):
    """
    话题有新评论时通知作者
    """
    try:
        topic = Topic.objects.get(id=comment.object_pk)
    except Topic.DoesNotExist:
        return
    if topic.author_id == comment.user_id:
        return
    pm_content = u"你发表的话题《%s》收到了新的回复：\n%s\
    \n详情请见- %s%s" %(topic.title,comment.comment,DOMAIN,topic.get_absolute_url())
    Pm(
        from_user = User.objects.get(id=1),
        to_user = topic.author,
        title = '话题动态',
        content = pm_content,
        system = True
    ).save()

def _code_notice(comment):
    try:
        code = Base.objects.get(id=comment.object_pk)
    except Base.DoesNotExist:
        return
    if code.author_id == comment.user_id:
        return
    pm_content = u"你分享的代码《%s》收到了新的评论：\n%s\
    \n详情请见- %s%s" %(code.title,comment.comment,DOMAIN,code.get_absolute_url())
    Pm(
        from_user = User.objects.get(id=1),
        to_user = code.author,
        title = '代码分享动态',
        content = pm_content,
        system = True
    ).save()

def _wiki_notice(comment):
    try:
        wiki = Entry.objects.get(id=comment.object_pk)
    except Entry.DoesNotExist:
        return
    if wiki.author_id == comment.user_id:
        return
    pm_content = u"你的文章《%s》收到了新的评论：\n%s\
    \n详情请见- %s%s" %(wiki.title,comment.comment,DOMAIN,wiki.get_absolute_url())
    Pm(
        from_user = User.objects.get(id=1),
        to_user = wiki.author,
        title = '文章动态',
        content = pm_content,
        system = True
    ).save()

def job_notice(sender,**kwargs):
    """ send a message to admin's account """
    Pm(
        from_user = User.objects.get(id=1),
        to_user = User.objects.get(id=1),
        title = '有新发布的招聘信息等待审核',
        content = 'http://pythoner.net/admin/jobs/job/{0}/'.format(kwargs['job'].id),
        system = True
    ).save()

def do_nothing(instance):
    pass

def welcome(sender,**kwargs):
    """
    用户注册后发送PM
    """
    content = "欢迎来到Python开发者社区，网站代码已经开源,欢迎Fork,http://github.com/tianyu0915/pythoner.net"
    to_user = kwargs['profile'].user
    Pm(
        from_user=User.objects.get(id=1),
        to_user=to_user,
        title='Welcome',
        content=content,
        system = True
    ).save()
    
    # 同时给管理员发送通知
    Pm(
        from_user = User.objects.get(id=1),
        to_user = User.objects.get(id=1),
        title = 'new user ',
        content = 'name:{0}'.format(kwargs['profile'].screen_name),
        system = True,
    ).save()


new_user_register.connect(welcome)
post_save.connect(comment_notice,sender=Comment)
new_job_was_post.connect(job_notice)
