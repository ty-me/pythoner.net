#encoding:utf-8
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
