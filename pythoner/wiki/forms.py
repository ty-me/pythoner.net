# -*- coding: utf-8 -*-
"""
pythoner.net
Copyright (C) 2013  PYTHONER.NET

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

