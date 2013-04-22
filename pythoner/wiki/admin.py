from django.contrib import admin
from wiki.models import *

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title','category','sub_time','click_time')
    list_display_links = ('title','category')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','remark')
    list_display_links = ('name','remark')

admin.site.register(Entry,EntryAdmin)
admin.site.register(Category)
admin.site.register(Tag,TagAdmin)
