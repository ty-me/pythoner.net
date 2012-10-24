# -*- coding: utf-8 -*-
# Data:11-7-21 上午10:17
# Author: T-y(master@t-y.me)
# File:admin

from django.contrib import admin
from models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('title','city','company','email','website','sub_time','display')
    ordering = ['display']

admin.site.register(Job,JobAdmin)