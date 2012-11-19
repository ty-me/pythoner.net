#encoding:utf-8
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
