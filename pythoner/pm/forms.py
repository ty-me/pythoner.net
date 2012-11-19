#encoding:utf-8
from django import forms
from pm.models import Pm

class PmForm(forms.ModelForm):
    class Meta:
        model = Pm
        fields = ('content',)
  