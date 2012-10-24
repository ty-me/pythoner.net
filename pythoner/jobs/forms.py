# -*- coding: utf-8 -*-
# Data:11-7-16 下午3:56
# Author: T-y(master@t-y.me)
# File:forms.py
from django import forms
from jobs.models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('display','click_times','city','ip')