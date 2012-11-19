# -*- coding: utf-8 -*-
# Data:11-8-8 下午9:32
# Author: T-y(master@t-y.me)
# File:signals
from django.dispatch import Signal

new_user_register = Signal(providing_args=['profile'])