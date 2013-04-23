# -*- coding: utf-8 -*-
# Data:11-7-26 下午7:16
# Author: T-y(master@t-y.me)
# File:fomrs
from django import forms
from wiki.models import Entry

class PostForm(forms.Form):
    source = forms.URLField(label='文章链接',required=True)

class UserWikiForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('category','title','content')

class WikiForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title','category','content','source')


class WikiMdForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title','category','md_content','source')

