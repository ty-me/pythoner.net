# -*- coding: utf-8 -*-
# Data:11-6-20 下午9:29
# Author: T-y(master@t-y.me)
# File:profile
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from forms import *
from PIL import Image
import datetime
import os
import urllib
from accounts.models import UserProfile
from settings import ROOT_PATH
from signals import photo_was_uploaded
from models import Visitor
from home.models import Develop
from accounts.models import Link

def index(request,u_id,page=1):
    """
    查看用户个人资料
    """

    # 初始化
    try:
        u_id = int(u_id)
    except :
        return HttpResponse(u_id)

    # 根据ID得到用户对象
    try:
        user = User.objects.get(id=u_id)
    except User.DoesNotExist:
        raise Http404()

    # 如果是当前用户自己则跳转到个人中心
    if request.user == user:
        return HttpResponseRedirect('/home/')
    elif request.user.is_authenticated():
        visitor,visitor_created= Visitor.objects.get_or_create(master=user,visitor=request.user)
        visitor.sub_time = datetime.datetime.now()
        visitor.save()
    # 得到用户档案
    try:
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile()
        profile.user = user
        profile.save()

    # 如果账号以删除
    if profile.deleted == True:
        return render('home_none.html',locals(),context_instance=RequestContext(request))

    develop_all = Develop.objects.filter(user=profile.user)
    paginator = Paginator(develop_all,15)
    url = 'home/%d' %profile.user.id
    current_page = 'develop'
    try:
        develops = paginator.page(page)
    except (EmptyPage,InvalidPage):
        develops = paginator.page(paginator.num_pages)

    return render('home_index.html',locals(),context_instance=RequestContext(request))

@login_required
def edit(request):
    """
    修改用户个人资料
    """
    current_page = 'profile-edit'
    profile = request.user.get_profile()
    # 处理GET请求
    if request.method == 'GET':
        form = ProfileForm(instance=profile)
        return render('home_edit.html',locals(),context_instance=RequestContext(request))

    # 处理POST请求
    form = ProfileForm(request.POST,instance=profile)
    if form.is_valid():
        new_profile = form.save()
        if new_profile.id:
            messages.success(request,'更新设置成功！')
        else:
            messages.error(request,'更新设置失败，请重试')
    else:
        messages.error(request,'数据无效，请检查')
    return render('home_edit.html',locals(),context_instance=RequestContext(request))

@login_required
def delete(request):
    """
    删除账号
    """
    current_page = 'profile-delete'
    # 处理POST请求
    if request.method == 'POST' and request.POST['submit']:
        profile = request.user.get_profile()
        profile.deleted = True
        profile.save()
        auth_logout(request)
        messages.success(request,'账号删除成功')

    return render('account_delete.html',locals(),context_instance=RequestContext(request))

@login_required
def photo(request):
    return HttpResponse('哦活，头像上床功能正在维护中...')

    current_page = 'profile-photo'
    profile = UserProfile.objects.get(user=request.user)

    # 处理GET请求
    if request.method == 'GET':
        form = PhotoForm()
        return render('home_photo_edit.html',locals(),context_instance=RequestContext(request))

    # 处理图片上传
    if request.method == 'POST':
        photo_name = '%sp.jpeg' %request.user.id
        icon_name = 'icon_%sp.jpeg' %request.user.id
        path = os.path.join('/var/pythoner.net/static/user/')
        photo_size = (300,300)
        icon_size = (48,48)

        # 如果上传了新图片
        if 'photo' in request.FILES:

            # 缩放并保存大头像
            photo = Image.open(request.FILES['photo'])
            # 剪裁缩略图
            photo.thumbnail(photo_size,Image.ANTIALIAS)
            # 保存图片
            photo.save(os.path.join(path,photo_name),'jpeg')
            del photo
            profile.photo = photo_name
            profile.save()
            messages.success(request,'上传新头像成功')

        # 剪裁小头像30*30px并保存
        try:
            x1 = int(request.POST['x1'])
            y1 = int(request.POST['y1'])
            x2 = int(request.POST['x2'])
            y2 = int(request.POST['y2'])
        except :
            x1 = y1 = 0
            x2 = y2 = 48

        # 防止出现x1=x2,y1=y2的情况出现
        if x1==x2 or y1==y2:
            messages.error(request,'请先选择要剪裁的头像区域')
            return HttpResponseRedirect('/home/photo/')

        p = (x1,y1,x2,y2)
        #return HttpResponse(str(p))

        im = Image.open(os.path.join(path,photo_name))
        # return HttpResponse(str(os.path.join(path,photo_name)))
        icon = im.crop(p)
        icon.thumbnail(icon_size,Image.ANTIALIAS)
        icon.save(os.path.join(path,icon_name),'jpeg')
        messages.success(request,'剪裁头像成功')
        del im,icon

        # 发送信号
        photo_was_uploaded.send(
            sender=profile.__class__,
            user = profile.user
        )

    else:
        messages.error(request,'请选择你要上传的图片')
    return HttpResponseRedirect('/home/photo/')

@login_required
def password(request):
    """
    修改用户密码
    """
    current_page = 'profile-password'
    if request.method == 'POST':
        raw_password = request.POST.get('raw_password','')
        new_password1 = request.POST.get('new_password1','')
        new_password2 = request.POST.get('new_password2','')

        if not request.user.check_password(raw_password):
            messages.error(request,'原始密码错误！')
        elif len(new_password1)<6 or len(new_password1)>30:
            messages.error(request,'新密码的长度不符合要求！')
        elif new_password1 <> new_password2:
            messages.error(request,'两次新密码输入不一致！')
        else:
            try:
                request.user.set_password(str(new_password2))
                request.user.save()
            except Exception,e:
                raise e
            auth_logout(request)
            messages.success(request,'密码修改成功！请使用新密码重新登录一次。')
            return HttpResponseRedirect('/accounts/login/?next=/home/')

    return render('profile_password.html',locals(),context_instance=RequestContext(request))

@login_required
@csrf_protect
def link(request):
    current_page = 'profile-link'
    douban,douban_created = Link.objects.get_or_create(user=request.user,type='douban')
    try:
        weibo,weibo_created = Link.objects.get_or_create(user=request.user,type='weibo')
    except:
        for i in Link.objects.filter(user=request.user,type='weibo'):
            i.delete()
    twitter,twitter_created = Link.objects.get_or_create(user=request.user,type='twitter')
    facebook,facebook_created = Link.objects.get_or_create(user=request.user,type='facebook')
    other1,other1_created = Link.objects.get_or_create(user=request.user,type='other1')
    other2,other2_created = Link.objects.get_or_create(user=request.user,type='other2')

    if request.method == 'GET':
        return render('home_link_edi.html',locals(),context_instance=RequestContext(request))

    # 处理POST
    douban.url = request.POST.get('douban_url','')
    weibo.url = request.POST.get('weibo_url','')
    twitter.url = request.POST.get('twitter_url','')
    facebook.url = request.POST.get('facebook_url','')
    other1.name = request.POST.get('name1','')
    other1.url = request.POST.get('name1_url','')
    other2.name = request.POST.get('name2','')
    other2.url = request.POST.get('name2_url','')

    try:
        douban.save()
        weibo.save()
        twitter.save()
        facebook.save()
    except Exception,e:
        messages.error(request,'服务器出现错误，请稍候再试')

    if other1.name and other1.url:
        try:
            urllib.urlopen(other1.url)
        except Exception:
            messages.error(request,u'你输入的链接%s有误，请检查' %other1.url)
        else:
            other1.save()
    if other2.name and other2.url:
        try:
            urllib.urlopen(other2.url)
        except Exception:
            messages.error(request,u'你输入的链接%s有误，请检查' %other2.url)
        else:
            other2.save()

    return HttpResponseRedirect('/home/link/')

    
