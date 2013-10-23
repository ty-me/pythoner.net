#encoding:utf-8
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

import time,datetime
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Redirect301
from django.shortcuts import render_to_response as render
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from settings import *
from models import *
from forms import WikiForm,WikiMdForm
from signals import new_wiki_was_post
from accounts.signals import update_user_repulation
from utils.logger import getlogger
log = getlogger(__name__)

@cache_page(60*60)
def list(request,page=1):
    """
    列表页
    """
    current_page = APP
    nowtime = datetime.datetime.now()
    pre_url = APP
    allow_category = True
    category_name = request.GET.get('category','').encode('utf-8')
    tag_name = request.GET.get('tag','').encode('utf-8')
    page_title   = category_name or tag_name or u'板报'

    if category_name:
        page_description = u'分享在在{}分类下的所有文章'
        suf_url = '?category=%s' %category_name
        title   = category_name
        try:
            category_obj = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise Http404()
        else:
            entry_all = Entry.objects.filter(public=True,sub_time__lt = nowtime,category=category_obj)
    elif tag_name:
        # close the category list
        allow_category = False
        page_description = u'分享在在{}标签下的所有文章'
        suf_url = '?tag=%s' %tag_name
    
        try:
            tag = Tag.objects.get(name = tag_name)
        except Tag.DoesNotExist:
            raise Http404()

        try:
            tag_obj = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            raise Http404()
        else:
            entry_all = Entry.objects.filter(public=True,sub_time__lt = nowtime,tag=tag_obj)
    else:
        page_description = u'由用户分享的所有文章'
        entry_all = Entry.objects.filter(public=True,sub_time__lt = nowtime)


    #按分页获取文章条目        
    paginator = Paginator(entry_all,20)

    try :
        entrys = paginator.page(page)
    except(InvalidPage,EmptyPage):
        entrys = paginator.page(paginator.num_pages)
    return render(LIST_PAGE,locals(),context_instance=RequestContext(request))

def tag(request,tag_name,page=1):
    """
    按标签显示条目
    """
    new_url = u'/wiki/p{}/?tag={}'.format(page,tag_name)
    return Redirect301(new_url)

def detail(request,id):
    """
    浏览文章详细内容
    """
    template_name = 'wiki_cache_%s.html'%id
    try:
        id = int(id)
    except Exception:
        raise Http404()
    
    current_page = APP
    nowtime = datetime.datetime.now()
    next = '/wiki/%d/' %(int(id))
    
    try:
        entry = Entry.objects.get(id = id)
    except Entry.DoesNotExist:
        raise Http404()
    
    page_title = u'{}-({})'.format(entry.title,entry.category)
    page_description = u'{}'.format(entry.title)
    if not entry.public and entry.author.id <> request.user.id:
        raise Http404()
    
    if entry.public:
        Entry.objects.filter(id=id).update(click_time=entry.click_time+1)
    return render(DETAIL_PAGE,locals(),context_instance=RequestContext(request))

@csrf_protect
def post(request):
    """
    匿名用户投稿
    """
    
    current_page = APP

    if request.method == 'GET':
        form = WikiForm()
        return render('wiki_post.html',locals(),context_instance=RequestContext(request))

    form = WikiForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        try:
            send_mail(u'投稿',u'文章链接：%s' %data['source'],'wiki@pythoner.net',['admin@pythoner.net'])
        except Exception:
            pass
        msg = '感谢你的投稿，链接已发送至管理员'
        return render('posted.html',locals(),context_instance=RequestContext(request))
    else:
        return render('wiki_post.html',locals(),context_instance=RequestContext(request))

@login_required
@csrf_protect
def add(request,editor='markdown'):
    """ 用户写新的文章 
    
    """

    current_page = 'user_wiki'

    if request.method == 'GET':
        backup_data = {}
        for k in ['title','content','md_content','source']:
            _k = 'backup_{}'.format(k)
            try:
                v = request.session.get(_k)
                backup_data[k] = v
            except:
                pass

        if editor == 'markdown':
            title = u'分享文章(使用MarkDown编辑器)'
            form = WikiMdForm()
            template = 'wiki_add_md.html'
        else:
            title = u'分享文章(使用富文本编辑器)'
            form = WikiForm()
            template = 'wiki_add.html'
        page_title = title
        form.initial = backup_data
        return render(template,locals(),context_instance=RequestContext(request))
    
    
    if editor == 'markdown':
        form = WikiMdForm(request.POST)
        tpl_name = 'wiki_add_md.html'
    else:
        form = WikiForm(request.POST)
        tpl_name = 'wiki_add.html'

    if form.is_valid():
        data = form.cleaned_data
        if not data.get('md_content') and not data.get('content'):
            messages.error(request,u'文章文章内容不能为空')
            return render(tpl_name,locals(),context_instance=RequestContext(request))

        new_wiki = Entry(**data)
        new_wiki.author = request.user
        
        try:
            new_wiki.save()
        except Exception,e:
            msg = u'保存文章时出错'
            log.error(msg + str(e.message ))
            return HttpResponse(msg)
        else:
            # 发送增加声望的信号
            update_user_repulation.send(
                    sender = __name__,
                    request = request,
                    message = u'分享文章成功',
                    user  = request.user,
                    action = 'add',
                    content_type = 'wiki',
                    title  = new_wiki.title,
                    url    = new_wiki.get_absolute_url(),
            )

            # 发送信号
            new_wiki_was_post.send(
                sender= new_wiki.__class__,
                wiki =  new_wiki,
            )

            # 清除备份数据
            _keys = request.session.keys()
            for k in ['title','content','md_content','source']:
                _k = 'backup_{}'.format(k)
                if _k in  _keys:
                    del request.session[_k]
            return HttpResponseRedirect('/wiki/%d/' %new_wiki.id)
    else:
        return render(tpl_name,locals(),context_instance=RequestContext(request))

@login_required
@csrf_protect
def edit(request,wiki_id):
    """ 用户编辑文章 """
    current_page = 'user_wiki'
    title = '修改文章'

    try:
        wiki_id = int(wiki_id)
    except ValueError:
        raise Http404()
    
    try:
        wiki = Entry.objects.get(id=wiki_id,author=request.user)
    except Entry.DoesNotExist:
        raise Http404()

    if wiki.md_content:
        template = 'wiki_add_md.html'
    else:
        template = 'wiki_add.html'

    if wiki.public:
        messages.error(request,u'文章已经发表，不允许被修改或删除')
        url = '/wiki/{}/'.format(wiki.id)
        return HttpResponseRedirect(url)

    
    # 处理GET请求
    if request.method == 'GET':
        form = WikiForm(instance=wiki)
        return render(template,locals(),context_instance=RequestContext(request))

    # 处理POST请求    
    if wiki.md_content:
        form = WikiMdForm(request.POST)
    else:
        form = WikiForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        for k,v in data.items():
            setattr(wiki,k,v)
        try:
            wiki.save()
        except Exception,e:
            messages.error(request,u'保存文章时出错：%s'%e)
            return HttpResponseRedirect('/home/wiki/')
        else:
            messages.success(request,u'修改成功！')

        return HttpResponseRedirect('/wiki/%d/' %wiki.id)
    else:
        return render(template,locals(),context_instance=RequestContext(request))

@login_required
def delete(request,wiki_id):
    """
    用户删除文章

    """
    try:
        wiki = Entry.objects.get(id=wiki_id,author=request.user)
        wiki_title = wiki.title
    except Entry.DoesNotExist:
        raise Http404()

    if request.user == wiki.author:
        try:
            wiki.delete()
            # 扣除声望
            profile = request.user.get_profile()
            profile.score -= 15
            profile.save()
        except Exception,e:
            pass
        else:
            # 发送增加声望的信号
            update_user_repulation.send(
                    sender = __name__,
                    request = request,
                    message = u'删除文章成功',
                    user  = request.user,
                    action = 'delete',
                    content_type = 'wiki',
                    title  = wiki_title,
                    url    = '/',
            )
        return HttpResponseRedirect('/wiki/')
    else:
        raise Http404
            
