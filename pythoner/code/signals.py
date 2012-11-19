# -*- coding: utf-8 -*-
# Data:11-8-11 下午5:36
# Author: T-y(master@t-y.me)
# File:signals

from django.dispatch import Signal

new_code_was_post = Signal(providing_args=['code'])