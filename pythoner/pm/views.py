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

from django.http import Http404,HttpRequest,HttpResponseRedirect
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.http import Http404
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from models import *
from forms import *

@login_required
def inbox(request,page=1):
    """
    pm收件箱
    """
    current = 'inbox'
    td1 = '来自'
    empty_msg = '你还木有收到新的PM'

    pre_url = 'pm/inbox'
    pm_all  = Pm.objects.filter(to_user=request.user,to_deleted=False)
    paginator = Paginator(pm_all,20)
    try:
        entrys = paginator.page(page)
    except (InvalidPage,EmptyPage):
        entrys = paginator.page(paginator.num_pages)

    return render('pm_box.html',locals(),context_instance=RequestContext(request))

@login_required
def outbox(request,page=1):
    """
    pm发件箱
    """
    current = 'outbox'
    td1 = '寄给'
    empty_msg = '木有寄出的PM'

    pre_url = 'pm/outbox'
    pm_all  = Pm.objects.filter(from_user=request.user,from_deleted=False)
    paginator = Paginator(pm_all,20)
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1

    try:
        entrys = paginator.page(page)
    except (InvalidPage,EmptyPage):
        entrys = paginator.page(paginator.num_pages)

    return render('pm_box.html',locals(),context_instance=RequestContext(request))

@login_required
def detail(request,p_id):
    """
    pm详细内容
    """
    # 获取上一页地址
    from_url = request.META.get('HTTP_PEFERER','/pm/')

    # id有限性验证
    try:
        p_id = int(p_id)
    except ValueError:
        return Http404()

    # 查看权限验证（只能查看自己发送或者收到的并且没有删除的PM）
    try:
        pm = Pm.objects.get(id=p_id,from_user=request.user,from_deleted=False)
    except Pm.DoesNotExist:
        try:
            pm = Pm.objects.get(id=p_id,to_user=request.user,to_deleted=False)
        except Pm.DoesNotExist:
            raise Http404()

    # 标记为已读
    pm.readed = True
    pm.save()

    # 处理GET请求
    if request.method == 'GET':
        entry = pm
        del pm
        return render('pm_detail.html',locals(),context_instance=RequestContext(request))

    # 处理POST请求
    replay = request.POST.get('replay',False)
    delete = request.POST.get('delete',False)
    if replay :
        return HttpResponseRedirect('/pm/write/?reply=%d' %p_id)
    elif delete :
        pm.delete()
        return HttpResponseRedirect(from_url)
    else:
        raise Http404()

@login_required
@csrf_protect
def write(request):
    """
    发送PM
    """

    to_id = request.GET.get('to',False)
    r_id = request.GET.get('reply',False)
    next = request.META.get('HTTP_REFERER','/')

    # 如果是回复
    if r_id:
        try:
            pm = Pm.objects.get(id=int(r_id),to_user=request.user)
        except (Pm.DoesNotExist):
            raise Http404()
        pm.title = u'Re:'+pm.title
        pm.content = u'\n\n\n----------------------------------------\n原文：%s' \
        %pm.content
        to_user = pm.from_user
        form = PmForm(instance=pm)
        del pm

    # 如果是新PM
    elif to_id:
        try:
            user = User.objects.get(id=int(to_id))
        except :
            raise Http404()

        # 不允许给自己发PM
        if int(to_id) == request.user.id:
            #raise Http404()
            messages.warning(request,'你不能给自己发送PM!')
            return HttpResponseRedirect(next)
        form = PmForm()
        to_user = user
        del user
    else:
        return HttpResponseRedirect('/pm/')

    # 处理GET
    if request.method =='GET':
        return render('pm_write.html',locals(),context_instance=RequestContext(request))

    # 处理POST
    form = PmForm(request.POST)

    # 如果给自己发PM
    if to_user == request.user:
        raise Http404()

    if form.is_valid():
        data = form.clean()
        pm = Pm()
        pm.title = data['content'][:20]
        pm.content = data['content']
        pm.from_user = request.user
        pm.to_user = to_user
        pm.readed = False
        pm.save()

        return HttpResponseRedirect('/pm/outbox/')
    else:
        return render('pm_write.html',locals(),context_instance=RequestContext(request))

@login_required
def delete(request):
    """
    循环删除多个PM
    """

    # 获取上一页面URL
    from_url = request.META.get('HTTP_REFERER','/pm/')

    # 处理GET请求
    if request.method == 'GET':
        return HttpResponseRedirect(from_url)

    if 'pm_id[]' in request.POST:
        id_list = request.POST.getlist('pm_id[]')
    else:
        return HttpResponseRedirect(from_url)
    
    # 循环删除
    for id in id_list:
        try:
            id = int(id)
        except ValueError:
            pass

        # 判断要删除的PM是否存在
        try:
            pm = Pm.objects.get(id=id)
        except Pm.DoesNotExist:
            return HttpResponse('你要删除的PM不存在')

        # 判断是否有权删除
        if pm.from_user.id != request.user.id and pm.to_user.id != request.user.id:
            return HttpResponse('亲，请不要进行危险的操作哦，我们已经记下你了...')

        if pm.to_user == pm.from_user ==request.user and pm.system == True:
            pm.delete()
            continue

        # 接收者删除PM
        if pm.to_user == request.user:
            pm.to_deleted = True

        # 发送者删除PM
        elif pm.from_user == request.user:
            pm.from_deleted = True
        else:
            return HttpResponse('亲，请不要进行危险的操作哦，...')
        pm.save()

        # 如果发送者和接收者都已经删除，则从数据库中删除
        if pm.from_deleted == pm.to_deleted == True:
            pm.delete()
    return HttpResponseRedirect(from_url)

