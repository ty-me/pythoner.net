#encoding:utf-8
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response as render
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from django.contrib import messages
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from main.verify.views import *
from others.apis.sphinxapi import *
from wiki.models import Entry  
from topic.models import Topic 
from code.models import Base 
from jobs.models import Job 
import settings
r = settings.DATABASES['default']['REDIS']

def autocomplete(request):
    """
    搜索栏关键字自动填充
    """
    value = r.get('wiki_titles')
    if not value:
    	value = [i.title for i in Entry.objects.all()]
        r.set('wiki_titles',value)
    
    data = request.POST.get('data','')
    res = set()
    print 'key',r.get('wiki_searchs')
    for title in eval(r.get('wiki_searchs')):
        if data and data in title:
            res.add(title)

    html = ''
    for re in res[:20]:
        li = """<div>%s</div>""" %re
        html += li
    return HttpResponse(html)

def search(request,name,page=0):
    """
    一个简单的站内搜索 
    """
    # TODO 加入其它模块内容的搜索,重新制作搜索框
    q = str(request.GET.get('q',''))
    if not name or not q:
        return render('search.html',locals(),context_instance=ContextRequest(request))
    elif name == 'wiki':
        key = 'wiki_searchs'
        value = r.get('wiki_searchs') or []
        value = value and eval(value) or []
        value.append(q)
        entry_all = Entry.objects.filter(title__contains=q,public=True).all()
        if entry_all:
            r.set(key,value)
        print 'entry',entry_all

    #按分页获取文章条目        
    paginator = Paginator(entry_all,20)

    try :
        entrys = paginator.page(page)
    except(InvalidPage,EmptyPage):
        entrys = paginator.page(paginator.num_pages)
    return render('search.html',locals(),context_instance=RequestContext(request))

def _search_by_sphinx(request,name):
    """
    sphinx 全文搜索，暂时不用
    """
    mode = SPH_MATCH_ALL
    host = 'localhost'
    port = 9312
    indexs = {
            'wiki':{'name':'wiki_entry','module':wiki,'module_name':'板报'},
            'topic':{'name':'topic_topic','module':topic,'module_name':'话题'},
            'code':{'name':'code_base','module':code,'module_name':'代码'},
            'job':{'name':'jobs_job','module':job,'module_name':'招聘'},
        }

    try:
        index = indexs[name]
    except KeyError:
        return HttpResponse(name)
        raise Http404()
    else:
        sphinx_index = index['name']
        module = index['module']

    q = str(request.GET.get('q',''))
    if not q:
        return Http404()
    cl = SphinxClient()
    cl.SetServer(host,port)
    cl.SetWeights([100,1])
    cl.SetMatchMode(mode)
    res = cl.Query(q,sphinx_index)
    ids = []
    for re in res['matches']:
        ids.append(re['id'])

    entrys = module.objects.filter(id__in=ids)
    return render('search.html',locals())

