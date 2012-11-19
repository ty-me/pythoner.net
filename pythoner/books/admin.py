# -*- coding: utf-8 -*-
# Data:11-7-21 上午10:17
# Author: T-y(master@t-y.me)
# File:admin

from django.contrib import admin
from models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('name','author','publish','isbn','taobao_url','display')

admin.site.register(Category)
admin.site.register(Book,BookAdmin)
