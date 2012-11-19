#encoding:utf-8
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from models import UserRlation,Develop

@login_required
def index(request,page=1):
    """
    用户中心
    """
    url = 'home'
    current_page = 'develop'
    profile = UserProfile.objects.get(user=request.user)
    relation_all = UserRlation.objects.filter(source_user=request.user)
    if relation_all.count() == 0:
        follows_id_list = [relation.target_user.id for relation in relation_all]
    follows_id_list = []
    follows_id_list.append(request.user.id) # 以便抽取自己的动态
    develop_all = Develop.objects.filter(user__in=follows_id_list)
    paginator = Paginator(develop_all,15)
    try:
        develops = paginator.page(page)
    except (EmptyPage,InvalidPage):
        develops = paginator.page(paginator.num_pages)
        
    return render('home_index.html',locals(),context_instance=RequestContext(request))

def members(request,page=1):
    """
    成员
    """
    member_all = User.objects.order_by('-id').filter(is_active=True)
    paginatior = Paginator(member_all,42)
    url = 'home/members'
    
    try:
        entrys = paginatior.page(page)
    except(EmptyPage,InvalidPage):
        entrys = paginatior.page(paginatior.num_pages)
    return render('account_members.html',locals(),context_instance=RequestContext(request))

def code(request,user_id,page=1):
    """
    用户发表的代码
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404()

    from code.models import Base

    url = 'home/%d/code' %user.id
    current_page = 'user_code'
    code_all = Base.objects.filter(display=True,author=user)
    paginator = Paginator(code_all,20)
    try:
        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)
    return render('home_code.html',locals(),context_instance=RequestContext(request))

def topic(request,user_id,page=1):
    from topic.models import Topic
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404()
    topic_all = Topic.objects.filter(author=user)
    paginator = Paginator(topic_all,20)
    url = 'home/%d/topic' %user.id
    current_page = 'user_topic'
    try:
        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)
    return render('home_topic.html',locals(),context_instance=RequestContext(request))