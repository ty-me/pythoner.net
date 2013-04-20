#encoding:utf-8
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
from DjangoVerifyCode import Code

@cache_page(60*60)
def index(request):
    topics = Topic.objects.filter(deleted=False).order_by('-id')[0:16]
    current_page = 'index'
    codes = Base.objects.filter(display=True).order_by('-id')[0:20]
    jobs = Job.objects.order_by('-sub_time').filter(display=True).order_by('-id')[0:15]
    wiki_first = Entry.objects.filter(public=True).order_by('-sub_time')[0]
    wiki_second = Entry.objects.filter(public=True).order_by('-sub_time')[1]
    wikis = Entry.objects.filter(public=True).exclude(id__in=[wiki_first.id,wiki_second.id]).order_by('-id')[0:20]
    response = render('index.html',locals(),context_instance=RequestContext(request))
    return response

def usernav(request):
    """
    返回一个sub nav
    """
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

def verify_code(request):
    code =  Code(request)
    code.type = 'number'
    return code.display()

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

