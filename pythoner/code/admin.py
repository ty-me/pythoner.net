# -*- coding: utf-8 -*-
# Data:11-8-6 下午2:13
# Author: T-y(master@t-y.me)
# File:admin
from django.contrib import admin
from code.models import Language
from code.models import Category
from code.models import Base

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name','suffix','brush','js')

class BaseAdmin(admin.ModelAdmin):
    list_display = ('title','category','author','sub_time','click_times','display')

admin.site.register(Language,LanguageAdmin)
admin.site.register(Category)
admin.site.register(Base,BaseAdmin)