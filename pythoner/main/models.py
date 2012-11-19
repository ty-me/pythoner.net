from django.db import models
from django.contrib.admin.models import User

class Gfw(models.Model):
    ip = models.IPAddressField('IP',default='127.0.0.1')
    user = models.ForeignKey(User,blank=True,null=True)
    sub_time = models.DateTimeField(auto_now_add=True)
