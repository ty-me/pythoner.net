# -*- coding: utf-8 -*-
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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