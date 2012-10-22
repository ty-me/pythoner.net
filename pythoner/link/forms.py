# -*- coding: utf-8 -*-
# Data:10-7-3 上午1:03
# Author: T-y(master@t-y.me)
# File:forms
from django import forms
from link.models import Link

class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        widgets = {'remark':forms.Textarea()}
        exclude = ('display','notice','sub_time')
