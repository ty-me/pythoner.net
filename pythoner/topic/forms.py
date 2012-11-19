# -*- coding: utf-8 -*-
# Data:11-6-17 下午7:20
# Author: T-y(master@t-y.me)
# File:forms
from django import forms

class TopicForm(forms.Form):
    title = forms.CharField(label='标题',min_length=3,max_length=50,required=True)
    content = forms.CharField(label='正文',required=True,widget = forms.Textarea(),help_text='')
