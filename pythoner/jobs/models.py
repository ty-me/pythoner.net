#encoding:utf-8
#author ty:master@t-y.me
from django.db.models.signals import post_save
from django.db import models
from django.core.mail import send_mail
from settings import DOMAIN

class Job(models.Model):
    display = models.BooleanField('显示',default=False)
    click_times = models.IntegerField('点击次数',default=0)
    sub_time = models.DateTimeField('时间',auto_now_add=True)

    title = models.CharField('标题',max_length=50,help_text='招聘信息标题,50个字符以内')
    city = models.CharField('城市',max_length=15,default='北京',help_text='填写所在城市的名称，如‘北京’')
    company= models.CharField('公司',max_length=20,help_text='填写公司名称,20个字符以内',unique=False)
    website = models.URLField('网站',verify_exists=False,help_text='请填写公司网站',null=False,blank=False,unique=False)
    email = models.EmailField('信箱',help_text='HR接收简历投递的电子信箱',unique=False)
    content = models.TextField('内容')

    def __unicode__(self):
        if self.display:
            return u'[%s]%s %s' %(self.city,self.company,self.title)
        else:
            return u'[待审核][%s]%s %s' %(self.city,self.company,self.title)

    def get_absolute_url(self):
        return u'/jobs/%d/' %self.id

    class Meta:
        verbose_name_plural = '招聘信息'

def notify_hr(sender,instance,**kwargs):
    # BUG 当管理员重新编辑了招聘内容后会重复发送邮件
    if instance.display and instance.click_times == 0:
        from_emal = 'jobs@pythoner.net'
        to_email = []
        to_email.append(instance.email)
        subject = "招聘信息发布成功-来自pythoner.net的通知邮件"
        url = DOMAIN+'/jobs/%d/' %instance.id
        msg = """
        你好， 你在'python开发者社区'(http://pythoner.net)发布的招聘信息"%s"已经通过了审核，详见：%s
        有任何疑问或者需要帮助请联系管理员:admin@pythoner.net
                                                    --- pythoner.net敬上
        """ %(instance.title,url)
        send_mail(subject,msg,from_emal,to_email,fail_silently=True)
    else:
        pass

post_save.connect(notify_hr,sender=Job)
