# -*- coding: utf-8 -*-
# Data:11-9-3 上午10:42
# Author: T-y(master@t-y.me)
# File:wiki.py
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from pythoner.wiki.models import Entry
from django.views.decorators.csrf import csrf_protect

def list(request,user_id,page=1):
    """
    用户发表的代码
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404()

    url = 'home/%d/wiki' %user.id
    current_page = 'user_wiki'
    wiki_all = Entry.objects.filter(author=user)
    paginator = Paginator(wiki_all,20)
    try:
        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)
    return render('home_wiki.html',locals(),context_instance=RequestContext(request))
