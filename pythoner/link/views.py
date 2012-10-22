#encoding:utf-8
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


