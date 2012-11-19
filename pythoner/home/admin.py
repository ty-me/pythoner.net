# -*- coding: utf-8 -*-
# Data:11-8-4 下午10:24
# Author: T-y(master@t-y.me)
# File:admin
from django.contrib import admin
from home.models import *

class RelationAdmin(admin.ModelAdmin):
    list_display = ('source_user','target_user','type')

class DevelopAdmin(admin.ModelAdmin):
    list_display = ('user','type','sub_time')


admin.site.register(UserRlation,RelationAdmin)
admin.site.register(Type)
admin.site.register(Develop,DevelopAdmin)
admin.site.register(Object)
admin.site.register(Visitor)