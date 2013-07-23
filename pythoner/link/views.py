#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.NET

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

from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from link.models import *
from link.forms import LinkForm

def index(request):
    return render('link_index.html',locals(),context_instance=RequestContext(request))

@csrf_protect
def add(request):

    # 处理GET请求
    if request.method == 'GET':
        form = LinkForm()
        return render('link_add.html',locals(),context_instance=RequestContext(request))

    # 处理POST请求
    form = LinkForm(request.POST)

    # 处理用户提交的数据
    if form.is_valid():
        form.save()
        return render('link_posted.html',locals(),context_instance=RequestContext(request))
    else:
        return render('link_add.html',locals(),context_instance=RequestContext(request))


