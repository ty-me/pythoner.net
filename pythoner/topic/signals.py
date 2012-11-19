# -*- coding: utf-8 -*-
# Data:11-8-5 下午2:34
# Author: T-y(master@t-y.me)
# File:signals
from django.dispatch import Signal

new_topic_was_posted = Signal(providing_args=['topic'])