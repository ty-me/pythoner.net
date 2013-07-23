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

from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from models import *
from forms import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from django.shortcuts import render_to_response as render
from main.verify.views import *
from signals import new_topic_was_posted
import datetime

def list(request,page=1):
    current_page = 'topic'
    topic = Topic()
    topic_all = topic.all()
    paginator = Paginator(topic_all,20)
    title = u'正在讨论'
    pre_url ='topic'
    tags = Tag.objects.all()
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        entrys = topics = paginator.page(page)
    except (InvalidPage,EmptyPage):
        entrys = topics = paginator.page(paginator.num_pages)
        
    return render('topic_index.html',locals(),context_instance=RequestContext(request))

def list_by_user(request,user_id,page=1):
    try:
        user = User.objects.get(id=1)
    except User.DoesNotExist:
        raise Http404()
    
    current_page = 'topic'
    topic_all = Topic.objects.filter(author=user,deleted=False)
    paginator = Paginator(topic_all,20)
    title = u'正在讨论'
    url ='topic'
    tags = Tag.objects.all()
    
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        entrys = topics = paginator.page(page)
    except (InvalidPage,EmptyPage):
        entrys = topics = paginator.page(paginator.num_pages)

    return render('topic_index.html',locals(),context_instance=RequestContext(request))

@login_required
@csrf_protect
def add(request):
    current_page = 'topic'
    title = '发起新话题'
    """
    写新的话题
    """

    form_action = '/topic/add/'
    if request.method == 'GET':
        form = TopicForm()
        return render('topic_edit.html',locals(),context_instance=RequestContext(request))

    form = TopicForm(request.POST)
    if form.is_valid():
        data = form.clean()
        new_topic = Topic(**data)
        new_topic.author = request.user
        new_topic.latest_response = datetime.datetime.now()
        new_topic.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
        try:
            new_topic.save()
        except Exception,e:
            messages.error(request,'服务器出现了错误，发表话题失败，请稍候重试')
            return render('topic_edit.html',locals(),context_instance=RequestContext(request))
        else:
            print 3
            #发送信号
            new_topic_was_posted.send(
                sender = new_topic.__class__,
                topic = new_topic
            )
        return HttpResponseRedirect('/topic/{0}/'.format(new_topic.id))

    # 数据有限性验证失败
    else:
        messages.error(request,'服务器出现了错误，发表话题失败，请稍候重试')
        return render('topic_edit.html',locals(),context_instance=RequestContext(request))

@csrf_protect
@login_required
def edit(request,topic_id):
    current_page = 'topic'
    title = '修改话题'
    """
    编辑话题
    """
    try:
        topic_id = int(topic_id)
        topic = Topic.objects.get(deleted=False,id=topic_id,author=request.user)
    except (ValueError,Topic.DoesNotExist):
        raise Http404()
    form_action = '/topic/%d/edit/' %topic.id
    # 处理GET请求
    if request.method == 'GET':
        print 'get.',topic.md_content
        form = TopicForm(initial={'title':topic.title,'md_content':topic.md_content})
        return render('topic_edit.html',locals(),context_instance=RequestContext(request))

    # 处理POST请求
    form = TopicForm(request.POST)
    if form.is_valid():
        data = form.clean()
        topic.title = data['title']
        topic.md_content = data['md_content']
        print 'reques.',request.POST.get('md_content')
        print 'data.',data['md_content']
        try:
            topic.save()
        except :
            messages.error(request,'服务器出现了错误，保存数据失败，请稍候再试')
            return render('topic_edit.html',locals(),context_instance=RequestContext(request))
        return HttpResponseRedirect('/topic/%d/' %topic.id)

    # 数据有效性验证失败
    else:
        return render('topic_edit.html',locals(),context_instance=RequestContext(request))

def delete(request,topic_id):
    current_page = 'topic'
    """
    删除话题
    """

    try:
        topic_id = int(topic_id)
        topic = Topic.objects.get(id=topic_id,author=request.user,deleted=False)
    except (ValueError,Topic.DoesNotExist):
        raise Http404()
    else:
        topic.deleted = True
        topic.save()
        set(request) # 记录用户操作次数
        return HttpResponseRedirect('/topic/')

def detail(request,topic_id):
    current_page = 'topic'
    """
    话题详细页面
    """
    next = '/topic/%d/' %int(topic_id)
    timestamp = time.time()
    try:
        topic_id = int(topic_id)
        topic = Topic.objects.get(id=topic_id,deleted=False)
    except (ValueError,Topic.DoesNotExist):
        raise Http404()
    topic.view()

    return render('topic_detail.html',locals(),context_instance=RequestContext(request))

def list_by_tag(request,tag_name):
    current_page = 'topic'
    """
    按标签列出话题
    """
    try:
        tag_name = tag_name
        tag = Tag.objects.get(name=tag_name)
    except (ValueError,Tag.DoesNotExist):
        raise Http404()
    try:
        page = int(request.GET.get('page',20))
    except ValueError:
        page = 1
    topic_all = Topic.objects.filter(tag=tag,deleted=False)
    paginator = Paginator(topic_all,1)
    title = u'标签：%s' %tag.name
    try:
        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)
    return render('topic_index.html',locals(),context_instance=RequestContext(request))

@login_required
def favorite(request):
    """
    用户收藏列表
    """

    favorite_all = Favorite.objects.all(user=request.user)
    paginator = Paginator(favorite_all,2)

    try:
        page = int(request.GET.get('page',20))
    except ValueError:
        page = 1

    try:
        entrys = favorites = paginator.page(page)
    except (InvalidPage,EmptyPage):
        entrys = favorites = paginator.page(paginator.num_pages)
    return render('topic_favorite.html',locals(),context_instance=RequestContext(request))

def favorite_mark(request,topic_id):
    """
    添加收藏(ajax方式)
    """

    # 判断数据提交方式
    if request.method == 'GET':
        return HttpResponseRedirect('/')

    # 验证用户是否登录
    if not request.user.id:
        return HttpResponse( "{'status':0}")

    # 验证话题是否存在
    try:
        topic_id = int(topic_id)
        topic = Topic.objects.get(id=topic_id,deleted=False)
    except (ValueError,Topic.DoesNotExist):
        return HttpResponse( "{'status':0}")


    try:
        favorite = Favorite.objects.get(topic=topic,user=request.user)

    # 如果没有收藏过 则将其收藏
    except Favorite.DoesNotExist:
        Favorite(user=request.user,topic=topic).save()
        return HttpResponse("{'status':1,'info':'Marked'}")

    # 如果用户已经收藏过 则将其删除
    else:
        favorite.delete()
        return HttpResponse("{'status':1,'info':'+ Mark'}")
