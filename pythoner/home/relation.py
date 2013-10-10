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

from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from models import UserRlation
from django.shortcuts import render_to_response as render

@login_required
def follow(request,target_id):
    next = str(request.META.get('HTTP_REFERER','/home/'))
    try:
        target_user = User.objects.get(id=target_id)
    except User.DoesNotExist:
        #return HttpResponse("{'status':0}")
        messages.error(request,'该用户不存在！')
        return HttpResponseRedirect(next)

    if request.user == target_user:
        messages.error(request,'不能关注你自己！')
        return HttpResponseRedirect(next)

    try:
        ship = UserRlation.objects.get(source_user=request.user,target_user=target_user)
    except UserRlation.DoesNotExist:
        ship1 = UserRlation(source_user=request.user,target_user=target_user)
        ship1.save() # 添加关注
        messages.success(request,'添加关注成功！')
        return HttpResponseRedirect(next)

    # 取消关注
    try:
        ship.delete()
    except Exception:
        messages.warning(request,'服务器出现故障，请稍候再试')
    else:
        messages.success(request,'取消关注成功！')
        
    return HttpResponseRedirect(next)

def follows(request,user_id):
    """
    得到用户关注的对象
    """
    current_page = 'follows'
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    follows = UserRlation.objects.filter(source_user=user,type='friend')
    return render('home_follows.html',locals(),context_instance=RequestContext(request))

def fans(request,user_id):
    """
    得到用户的粉丝
    """
    current_page = 'fans'
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    fans = UserRlation.objects.filter(target_user=user,type='friend')
    return render('home_fans.html',locals(),context_instance=RequestContext(request))