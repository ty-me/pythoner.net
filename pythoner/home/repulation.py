# -*- coding: utf-8 -*-
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.views.decorators.csrf import csrf_protect
from accounts.models import Repulation

def list(request,user_id,page=1):
    """
    用户声望变化的历史记录
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404()

    pre_url = 'home/%d/repulation' %user.id
    current_page = 'user_repulation'
    items_all = Repulation.objects.filter(user=user).order_by('-created_at')
    paginator = Paginator(items_all,20)
    try:
        items = paginator.page(page)
    except (EmptyPage,InvalidPage):
        items = paginator.page(paginator.num_pages)
    return render('home_repulation.html',locals(),context_instance=RequestContext(request))
