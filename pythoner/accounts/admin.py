# -*- coding: utf-8 -*-
# Data:11-7-11 下午1:04
# Author: T-y(master@t-y.me)
# File:admin
from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('screen_name','city','introduction')

admin.site.register(UserProfile,ProfileAdmin)