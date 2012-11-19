# -*- coding: utf-8 -*-
# Data:11-8-11 下午5:36
# Author: T-y(master@t-y.me)
# File:signals

"""
定义一个信号
"""

from django.dispatch import Signal
new_wiki_was_post = Signal(providing_args=['wiki'])

