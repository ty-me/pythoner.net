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

from settings import *
from django.db import models
from django.contrib.auth.models import User
import datetime,time
from settings import APP
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from signals import new_wiki_was_post
import markdown

class Category(models.Model):
    """
    内容分类
    """
    name = models.CharField(APP_NAME+'分类名称',max_length=20,unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/p1/?category=%s' %(APP,self.name)

    class Meta:
        verbose_name_plural=APP_NAME+'分类'

class Tag(models.Model):
    """
    标签
    """
    name = models.CharField('tagname',max_length=10,unique=True)
    remark = models.CharField('remark',max_length=300,blank=True,null=True)

    def __unicode__(self):
        return self.name 

    def get_absolute_url(self):
        return '/%s/tag/%s/p1/' %(APP,self.name)

    def save(self):
        self.name = self.name.strip()
        super(Tag,self).save()

    class Meta:
        verbose_name_plural=APP_NAME+'标签'

class Entry(models.Model):
    """
    文章
    """
    title         = models.CharField('标题',max_length=300)
    category      = models.ForeignKey(Category,verbose_name='分类',default=1)
    plink         = models.CharField('永久链接',max_length=15,blank=True,null=True)
    public        = models.BooleanField('公开',default=False)
    content       = models.TextField('内容')
    md_content    = models.TextField('MarkDown内容',default='',blank=True,null=True)
    author        = models.ForeignKey(User,verbose_name='作者',default=1)
    sub_time      = models.DateTimeField(default=datetime.datetime.now)
    allow_comment = models.BooleanField('允许回复',default=True)
    source        = models.URLField('转载来源(没有可不填)',default='',blank=True,null=True,verify_exists=False)
    click_time    = models.PositiveIntegerField('点击次数',max_length = 10,blank=True,null=True,default=0)
    tag           = models.ManyToManyField(Tag,verbose_name=APP_NAME+'标签',blank=True,null=True)
    image_urls    = models.CharField('图片',max_length=1000,default='',blank=True,null=True)


    def save(self,*args,**kwargs):
        if self.md_content:
            self.content = markdown.markdown(self.md_content)

        super(Entry,self).save(*args,**kwargs)

    def search(self,kw):
        """ search from title or content """
        result = []
        res = self.objects.filter(public=True,title__in=kw.order_by('-sub_time'))
        result += res

        res = self.objects.filter(public=True,content__in=kw.order_by('-sub_time'))
        result += res
        return list(set(result))

    def get_image_urls(self):
        if self.image_urls:
            return self.image_urls.split(',')
        else:
            return []

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%d/' %(APP,self.id)

    class Meta:
        ordering = ['public','-sub_time']
        verbose_name_plural=APP_NAME+'条目'

