#encoding:utf-8
#file:定时执行任务脚本
import sys
import threading
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.email.views import send_email
from django.contrib.auth.models import User
from django.template import loader
from wiki.models import Entry
from code.models import Base
from jobs.models import Job
import datetime
import time
import math


class SendToUser(object):
    """
    向不经常登录的用户发送电子邮件
    """
    max_touser_count = 10

    now = time.time()
    sub = 60*60*24*10
    date2 = datetime.date.fromtimestamp(now-sub)
    user_objects = [ user for user in User.objects.filter(last_login__lt=date2) ]
    #user_objects = [ user for user in User.objects.filter(id=132) ]
    wikis = Entry.objects.filter(public=True).order_by('-id')[:10]
    codes = Base.objects.filter(display=True).order_by('-id')[:10]
    jobs = Job.objects.filter(display=True).order_by('-id')[:5]
    html = loader.render_to_string('email_rss.html',
                                                {'wikis':wikis,'codes':codes,'jobs':jobs})   

    def __init__(self):
        pass

    def _get_user_objects(self,count=10):
        """ 得到指定数目的用户对象 """
        re = []
        try:
            for i in range(self.max_touser_count):
                re.append(self.user_objects.pop())
        except Exception:
            pass
        finally:
            return re

    def _get_to_user_list(self):
        """ 构造收件人列表 """
        self._to_user_list = [user.username for user in self._get_user_objects()]
        

    def run(self):
        while len(self.user_objects) > 0:
            self._get_to_user_list()
        
            print 'sending...'
            try:
                send_email('由pythoner.net为您推荐的内容',
                           self.html,
                           'accounts@pythoner.net',
                           self._to_user_list,
                           )

            except Exception,e:
                print 'error:',e
            print 'success'
            time.sleep(5)


mail = SendToUser()
mail.run()
