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

class Category(models.Model):
    """
    内容分类
    """
    name = models.CharField('分类名称',max_length=20,unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/book/%s/' %self.name

    class Meta:
        verbose_name_plural='分类'

class Book(models.Model):
    name = models.CharField('书名',max_length=40,blank=False,null=False)
    category = models.ForeignKey(Category,verbose_name='分类',default=1)
    author = models.CharField('作者',max_length=100,blank=False,null=False)
    translator = models.CharField('译者',max_length=100,blank=True,null=True)
    publish = models.CharField(max_length=50,blank=False,null=False)
    pub_date = models.CharField('出版日期',blank=False,null=False,max_length=10,default='2012年')
    instrution = models.TextField('介绍',help_text="图书简介、内容摘要")
    taobao_url = models.URLField('淘宝推广链接',blank=True,null=True)
    click_time = models.PositiveIntegerField('点击次数',max_length=10,default=0)
    price = models.FloatField('价格',default=0.00,blank=False,null=False)
    pages = models.PositiveIntegerField('页数',max_length=5,default=0,blank=False,null=False)
    isbn = models.CharField('ISBN',max_length=15,null=False,blank=False,unique=True)
    douban_id = models.PositiveIntegerField('豆瓣ID',max_length=15,null=False,blank=False,unique=True)
    display = models.BooleanField('显示',default=False)


    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/books/%d/' %int(self.isbn)

    class Meta:
        verbose_name_plural="图书"
