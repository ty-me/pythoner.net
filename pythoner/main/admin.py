# -*- coding: utf-8 -*-
# Data:11-9-18 下午2:45
# Author: T-y(master@t-y.me)
# File:admin
from django.contrib import admin
from main.models import Gfw

class GfwAdmin(admin.ModelAdmin):
    list_display = ('ip','user','sub_time')

admin.site.register(Gfw,GfwAdmin)
