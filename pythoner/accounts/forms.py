#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  TY<tianyu0915@gmail.com>

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
from models import UserProfile

class RegisterForm(forms.Form):
    """
    账号注册表单
    """
    username = forms.EmailField(label='信箱',help_text='填写正确的Email以便激活你的账户')
    screen_name = forms.CharField(label='昵称',required=True,max_length=20,min_length=3,help_text='长度在3~30个字符以内')
    password = forms.CharField(label='密码',required=True,max_length=20,min_length=6,help_text='长度在6~30个字符以内',widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.EmailField(label='信箱',required=True,max_length=30,min_length=3)
    password = forms.CharField(label='密码',required=True,max_length=128,min_length=6,
                               widget=forms.PasswordInput(),help_text='')
