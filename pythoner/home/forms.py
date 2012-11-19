#encoding:utf-8
from django import forms
from accounts.models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {'introduction':forms.Textarea()}
        exclude = ('score','deleted','photo','user','city')

class PhotoForm(forms.Form):
    photo = forms.ImageField(label='',max_length=1024)