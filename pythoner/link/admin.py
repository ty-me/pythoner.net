# -*- coding: utf-8 -*-
# Data:11-7-11 下午12:34
# Author: T-y(master@t-y.me)
# File:admin
from django.contrib import admin
from models import *

class LinkAdmin(admin.ModelAdmin):
    list_display = ('category','title','url','email','sub_time','display')
    list_display_links = ('title','category')

admin.site.register(Category)
admin.site.register(Link,LinkAdmin)
