# -*- coding: utf-8 -*-
# Data:11-7-27 上午10:43
# Author: T-y(master@t-y.me)
# File:forms
from django import forms
from models import Base
from models import Code
from models import Language

class CodeBaseForm(forms.ModelForm):
    description = forms.CharField(label='描述',help_text='代码相关的模块或者包名，多个请以空格隔开（选填）',
                             widget=forms.Textarea(),required=False)
    module = forms.CharField(label='模块',help_text='填写所需的模块名称，多个请以空格隔开（选填）',required=False)
    class Meta:
        model = Base
        fields = ('category','title')

class PasteForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('language','content')

class FileForm(forms.Form):
    file = forms.FileField(max_length=1024*1024*4,label='选择文件',help_text='你可以上传.py，.rar，.zip文件')