# -*- coding: utf-8 -*-
# Data:11-7-11 下午12:42
# Author: T-y(master@t-y.me)
# File:admin.py
from django.contrib import admin
from models import Pm

class PmAdmin(admin.ModelAdmin):
    list_display = ('system','title','from_user','from_deleted','to_user','to_deleted','sub_time','readed')
    list_display_links = ('title',)

admin.site.register(Pm,PmAdmin)