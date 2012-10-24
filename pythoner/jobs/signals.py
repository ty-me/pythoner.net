# -*- coding: utf-8 -*-
# Data:2010-8-11 下午5:58
# Author: admin@pythoner.net
# File:signals
from django.dispatch import Signal

new_job_was_post = Signal(providing_args=['job'])
