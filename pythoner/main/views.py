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

import time
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from topic.models import Topic
from link.models import Link
from wiki.models import Entry
from code.models import Base
from jobs.models import Job
from django.views.decorators.cache import cache_page
from main.models import Gfw
from code.models import Base

#@cache_page(60*60)
def index(request):
    current_page = 'index'
    page_title   = u'首页'
    topics       = Topic.objects.filter(deleted=False).order_by('-id')[0:16]
    codes        = Base.objects.filter(display=True).order_by('-id')[0:20]
    jobs         = Job.objects.order_by('-sub_time').filter(display=True).order_by('-id')[0:15]
    wiki_first   = Entry.objects.filter(public=True).order_by('-sub_time')[0]
    wiki_second  = Entry.objects.filter(public=True).order_by('-sub_time')[1]
    wikis        = Entry.objects.filter(public=True).exclude(id__in=[wiki_first.id,wiki_second.id]).order_by('-id')[0:20]


    from accounts.signals import update_user_repulation
    from django.contrib.auth.models import User
    update_user_repulation.send(
            sender = __name__,
            user  = User.objects.get(pk=1),
            action = 'add',
            content_type = 'wiki',
            title  = 'test signal',
            message = u'分享文章成功',
            url    = '/',
            request = request,
    )
    return render('index.html',locals(),context_instance=RequestContext(request))

def usernav(request):
    return render('user.nav.html',locals(),context_instance=RequestContext(request))

@cache_page(60*60*24)
def random(request,current_page=False):
    import random
    url = list()
    wiki = Entry.objects.order_by('?').filter(public=True)[0]
    url.append(wiki.get_absolute_url())
    topic = Topic.objects.order_by('?').filter(deleted=False)[0]
    url.append(topic.get_absolute_url())
    link = Link.objects.order_by('?').filter(display=True)[0]
    url.append(link.get_absolute_url())

    #return HttpResponse(str(url))
    return HttpResponseRedirect(random.sample(url,1)[0])

@cache_page(60*60)
def search(request):
    current_page = 'search'
    return render('search.html',locals(),context_instance=RequestContext(request))

@cache_page(60*60)
def plink(request,link):
    """
    处理永久链接
    """
    try:
        link = str(link)
    except ValueError:
        raise Http404()

    try:
        entry = Entry.objects.get(plink=link)
    except Entry.DoesNotExist:
        raise Http404()
    return render('custom.html',locals(),context_instance=RequestContext(request))


def email_rss(request):
    """
    emal订阅
    """

    style = str(request.GET.get('style',1))

    wikis = Entry.objects.filter(public=True)[:10]
    topics = Topic.objects.filter(deleted=False)[:10]
    codes = Base.objects.filter(display=True)[:10]
    jobs = Job.objects.filter(display=True).order_by('-id')[:10]
    return render('email_rss%s.html' %style,locals(),context_instance=RequestContext(request))

def fuck(request):
    """ Fuck Gfw """
    if request.method == 'GET':raise Http404()
    gfw = Gfw()
    gfw.ip = request.META['REMOTE_ADDR']
    gfw.user = request.user
    try:
        gfw.save()
    except Exception:
        pass

    if request.user.is_authenticated():
        profile = request.user.get_profile()
        profile.score = 1 + profile.score
        profile.save()

    your_count = Gfw.objects.filter(ip=request.META['REMOTE_ADDR']).count()
    total_count = Gfw.objects.all().count()
    info = 'GFW已被深深地Fuck了%d次，你贡献了%d次 你的账号积分增加为：%d' %(total_count,your_count,profile.score)
    return HttpResponse("{'status':1,'info':'%s'}" %info)

