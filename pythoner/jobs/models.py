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


from django.db.models.signals import post_save
from django.db import models
from django.core.mail import send_mail
from settings import DOMAIN

class Job(models.Model):
    display = models.BooleanField('显示',default=False)
    click_times = models.IntegerField('点击次数',default=0)
    sub_time    = models.DateTimeField('时间',auto_now_add=True)

    title       = models.CharField('标题',max_length=50,help_text='招聘信息标题,50个字符以内')
    city        = models.CharField('城市',max_length=15,default='北京',help_text='填写所在城市的名称，如‘北京’')
    company     = models.CharField('公司',max_length=20,help_text='填写公司名称,20个字符以内',unique=False)
    website     = models.URLField('网站',verify_exists=False,help_text='请填写公司网站',null=False,blank=False,unique=False)
    email       = models.EmailField('信箱',help_text='HR接收简历投递的电子信箱',unique=False)
    content     = models.TextField('内容')
    is_expired  = models.BooleanField('已过期',default=False)
    is_noticed  = models.BooleanField('已通知hr',default=False)

    def __unicode__(self):
        if self.display:
            return u'[%s]%s %s' %(self.city,self.company,self.title)
        else:
            return u'[待审核][%s]%s %s' %(self.city,self.company,self.title)

    def save(self,*args,**kwargs):
        if self.id and self.display and not self.is_noticed:
            from_emal = 'admin@pythoner.net'
            to_email = []
            to_email.append(self.email)
            subject = u"招聘信息发布成功-来自[Python开发者社区]的通知邮件"
            url = DOMAIN+'/jobs/%d/' %self.id
            msg = u"""
            你好， 你在'Python开发者社区'(http://pythoner.net)发布的招聘信息"%s"已经通过了审核，详见：%s
            有任何疑问或者需要帮助请联系管理员:admin@pythoner.net
                                                        --- Python开发者社区 敬上
            """ %(self.title,url)
            send_mail(subject,msg,from_emal,to_email,fail_silently=True)
            self.is_noticed = True

        return super(Job,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return u'/jobs/%d/' %self.id

    class Meta:
        verbose_name_plural = '招聘信息'

