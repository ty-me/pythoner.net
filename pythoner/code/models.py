#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.NET

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

class Language(models.Model):
    name = models.CharField('语言',max_length=50,unique=True)
    suffix = models.CharField('后缀',max_length=10,blank=True,null=True,default='')
    brush = models.CharField('刷子',max_length=50)
    js = models.CharField('刷子js文件',max_length=50)

    class Meta:
        ordering = ['-name']
        verbose_name_plural='语言包'

    def save(self):
        self.name = self.name.strip() # 去掉两边空格
        self.suffix = self.suffix.strip() # 去掉两边空格
        self.brush = self.brush.strip() # 去掉两边空格
        self.js = self.js.strip() # 去掉两边空格
        super(Language,self).save()

    def __unicode__(self):
        return self.name

class Module(models.Model): 
    name = models.CharField('模块名',max_length=30)

    def __unicode__(self):
        return self.name 

    class Meta:
        verbose_name_plural='模块名'


    def save(self):
        self.name = self.name.strip().lower() # 去掉两边空格
        super(Module,self).save()

class Category(models.Model): 
    """
    代码分类
    """
    name = models.CharField('分类',max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '代码分类'


    def get_absolute_url(self):
        return '/code/p1/?category=%s' %self.name

class Base(models.Model):
    category = models.ForeignKey(Category,verbose_name='分类',default=1)
    author = models.ForeignKey(User,verbose_name='作者',blank=True,null=True)
    title = models.CharField('标题',max_length=100,
                             help_text='一句话概括代码的用途（例：使用 jsoup 从 HTML 中提取所有链接的例子）')
    description =models.CharField('描述',max_length=500)
    module = models.ManyToManyField(Module,verbose_name='相关模块',blank=True,null=True,help_text='(选填)')
    sub_time = models.DateTimeField('时间',auto_now_add=True)

    click_times = models.PositiveIntegerField('点击次数',max_length=10,default=0)
    display = models.BooleanField('是否显示',default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/code/%d/' %self.id

    def view(self):
        self.click_times +=1
        self.save()

    class Meta:
        ordering = ['-id']
        verbose_name_plural='代码信息'

class Code(models.Model):
    """
    源代码
    """
    base = models.ForeignKey(Base)
    language = models.ForeignKey(Language,verbose_name='语言',default=1)
    name = models.CharField('代码名称',max_length=50,blank=True,null=True)
    content = models.TextField('Code')

    def __unicode__(self):
        return self.base.title 

    class Meta:
        verbose_name_plural='源码'

class Zip(models.Model):
    base = models.ForeignKey(Base)
    name = models.CharField('文件名',max_length=50,blank=True,null=True)
    file = models.BooleanField('压缩包',max_length=50,default=False)
    size = models.PositiveIntegerField('尺寸(bit)',max_length=10)
    download_times = models.PositiveIntegerField('下载次数',max_length=10,default=0)

class Visitor(models.Model):
    """
    最近查看代码的人
    """
    base = models.ForeignKey(Base)
    user = models.ForeignKey(User,related_name='code_visitor')
    sub_time = models.DateTimeField(auto_now=True)
