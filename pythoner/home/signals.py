# -*- coding: utf-8 -*-
# Data:11-8-5 上午10:34
# Author: T-y(master@t-y.me)
# File:signals
from django.dispatch import Signal

# 当用户更新了状态
status_was_posted = Signal(providing_args=['user'])

# 更新头像
photo_was_uploaded = Signal(providing_args=['user'])
