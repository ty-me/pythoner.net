#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  TY<tianyu0915@gmail.com>

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

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.template import loader
from main.verify.views import *
from forms import *
from models import UserProfile
from settings import DOMAIN
from accounts.signals import new_user_register
from main.email.views import send_email
import hashlib

TURN_OFF = False
@csrf_protect
def register(request):
    """
    新用户注册
    """

    if request.method == 'GET':
        if TURN_OFF:
            return render('account_register_off.html',locals())
        else:
            form = RegisterForm()
            return render('account_register.html',locals(),context_instance=RequestContext(request))

    return _register(request)

def _register(request):
    """
    用户注册
    """
    form = RegisterForm(request.POST)
    zen  = request.POST.get('zen')

    if not zen:
        messages.error(request,'对不起，你没有同意《The Zen Of Python》,暂时不能加入')
        return render('account_register.html',locals(),context_instance=RequestContext(request))

    if form.is_valid():
        data = form.clean()
    else:
        return render('account_register.html',locals(),context_instance=RequestContext(request))

    # 检查email是否存在
    try:
        user = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        pass
    else:
        messages.error(request,'email已经注册过，请换一个')
        return render('account_register.html',locals(),context_instance=RequestContext(request))

    # 创建新用户
    new_user = User.objects.create_user(username=data['username'],email=data['username'],
                                        password=data['password'])
    new_user.is_active = False
    new_user.save()
    new_profile = UserProfile(user=new_user,screen_name=data['screen_name'])

    try:
        new_profile.save()
        return HttpResponseRedirect('/accounts/active/%d/not_active/' %new_user.id)
    except Exception,e:
        messages.error(request,'服务器出现错误：%s' %e)

    return render('account_register.html',locals(),context_instance=RequestContext(request))

@csrf_protect
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    if request.method == 'GET':

        referer  = request.META.get('HTTP_REFERER','/')
        if not 'accounts' in str(referer) :
            request.session['referer'] = referer
        else :
            request.session['referer'] = '/'
        form = LoginForm()
        return render('account_login.html',locals(),context_instance=RequestContext(request))
    

    print 'post data',request.POST
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.clean()

        # 检查email是否存在
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            messages.error(request,"这个email还没注册过，<a href=\"/accounts/register/\">果断注册</a>")
            return render('account_login.html',locals(),context_instance=RequestContext(request))

        user = authenticate(username=data['username'],password=data['password'])
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                next = request.GET.get('next',False) or request.session['referer'] # 下页地址
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect('/accounts/active/%d/%s/' %(user.id,'not_active'))
        else:
            messages.error(request,'密码错误！')

    return render('account_login.html',locals(),context_instance=RequestContext(request))

def logout(request):
    """
    退出登录
    """
    auth_logout(request)
    request.session['access_token'] = ''
    request.session['request_token'] = ''
    return HttpResponseRedirect('/')

def active(request,u_id,active_code):
    """
    用户账号激活处理
    """
    # XXX

    try:
        u_id = int(u_id)
        user = User.objects.get(id=u_id)
    except (User.DoesNotExist,ValueError):
        return HttpResponseRedirect('/')

    # 已经激活过
    if user.is_active:
        messages.success(request,'账号已经激活，请直接登录')
        return HttpResponseRedirect('/accounts/login/')

    # 验证激活码是否正确
    elif active_code == _get_active_code(user.email):
        user.is_active = True
        user.save()
        messages.success(request,'恭喜，账号激活成功！马上登录，体验一下吧。')

        # 发送信号
        new_user_register.send(
            sender=user.get_profile().__class__,
            profile = user.get_profile()
        )
        return HttpResponseRedirect('/accounts/login/')
    elif active_code == 'not_active':

        active_url = '%s/accounts/active/%d/%s/' %(DOMAIN,user.id,_get_active_code(user.username))
        subject = 'Python开发者社区-账号激活邮件'
        body = loader.render_to_string('account_active.email.html',{'user':user,'active_url':active_url})
        from_email = 'accounts@pythoner.net'
        to = [user.username]
        # 开启发送激活邮件线程
        send_email(subject,body,from_email,to)

        #  根据邮件地址找到信箱登录地址
        email_domains = {
            'qq.com':'mail.qq.com',
            'foxmail.com':'mail.qq.com',
            'gmail.com':'www.gmail.com',
            '126.com':'www.126.com',
            '163.com':'www.163.com',
            '189.cn':'www.189.cn',
            '263.net':'www.263.net',
            'yeah.net':'www.yeah.net',
            'sohu.com':'mail.sohu.com',
            'tom.com':'mail.tom.com',
            'hotmail.com':'www.hotmail.com',
            'yahoo.com.cn':'mail.cn.yahoo.com',
            'yahoo.cn':'mail.cn.yahoo.com',
            '21cn.com':'mail.21cn.com',
        }

        for key,value in email_domains.items():
            print user.username.count(key)
            if user.username.count(key) >= 1:
                email_domain = value
                break

        return render('account_active.html',locals(),context_instance=RequestContext(request))
    else:
        raise Http404()

def _get_active_code(email):
    """
    计算激活码
    """
    #TODO:代码开源了之后用户可以根据这里计算出激活码，为防止破解
    #     可随机生成激活码后存入数据库。有时间了优化这里
    date_str = time.strftime('%Y-%m-%d',time.localtime()) # 当天内有效
    m = hashlib.md5(str(email)+'pythoner.net'+'axweraf9092443lklnfd0f89dmrej'+date_str)
    return m.hexdigest()

