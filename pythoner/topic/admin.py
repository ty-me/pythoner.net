# -*- coding: utf-8 -*-
# Data:11-7-11 下午12:39
# Author: T-y(master@t-y.me)
# File:admin
from django.contrib import admin
from models import *

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','author','sub_time','latest_response','click_times')

admin.site.register(Topic,TopicAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)