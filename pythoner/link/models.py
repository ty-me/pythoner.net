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
from django.core.mail import send_mail

class Category(models.Model):
    name = models.CharField('类别',max_length=10)

    def __unicode__(self):
        return self.name
   
    class Meta:
        verbose_name_plural = '链接分类'

class Link(models.Model):
    category = models.ForeignKey(Category,verbose_name='类别',null=True,blank=True)
    url = models.URLField('网址',unique=True,verify_exists=False)
    title = models.CharField('标题',unique=True,max_length=15)
    email = models.EmailField('邮件')
    remark = models.CharField('说明',max_length=100)
    display = models.BooleanField('显示',default=False)
    sub_time = models.DateTimeField('时间',auto_now_add=True)

    def get_absolute_url(self):
        return self.url

    class Meta: 
        ordering = ['display','-id']
        verbose_name_plural = '链接信息'

    def __unicode__(self):
        if self.display:
            return u'[%s] %s:%s' %(self.category.name,self.title,self.url)
        else:
            return u'[待审核]%s:%s' %(self.title,self.url)
