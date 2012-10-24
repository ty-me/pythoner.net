# -*- coding: utf-8 -*-
# Data:11-7-21 下午12:59
# Author: T-y(master@t-y.me)
# File:jobs_tags
from django.template import Library
from jobs.models import Job

register = Library()

@register.inclusion_tag('jobs_latest.tag.html')
def get_latest_job(count=10):
    """
    最近的招聘信息
    """
    return {'jobs':Job.objects.filter(display=True).order_by('-id')[:count]}

@register.inclusion_tag('jobs_click.tag.html')
def get_job_by_click_time(count=10):
    return {'jobs':Job.objects.filter(display=True).order_by('-click_times')[:count]}