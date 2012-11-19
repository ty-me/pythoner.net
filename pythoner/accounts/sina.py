#encoding:utf-8
# Data:11-6-29 下午9:59
# Author: T-y(master@t-y.me)
# File:sina
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from models import UserProfile
from models import Link
from weibo import APIClient
from accounts.signals import new_user_register
import settings


APP_KEY = settings.WEIBO_APP_KEY
APP_SECRET = settings.WEIBO_APP_SECRET
CALLBACK_URL = settings.WEIBO_CALLBACK_URL
client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)


def index(request):
    """
    跳转到验证页面
    """
    auth_url = client.get_authorize_url()
    return HttpResponseRedirect(auth_url)

def callback(request):
    """
    用户授权后的回调
    """
    code = request.GET.get(u'code')
    #client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
    res = client.request_access_token(code)
    access_token = res['access_token']
    expires_in = res['expires_in']
    # 可以不保存用户的access token,因为不会在其它地方操作用户数据
    request.session['access_token'] = access_token
    request.session['expires_in'] = expires_in
    client.set_access_token(access_token,expires_in)
    uid = client.get.account__get_uid()['uid']
    # 设置成一个特殊的用户名（非email格式），正常的登陆表单是需要验证用户名为email格式，这里
    # 将用户名设置成非email格式，可以微博用户通过账号密码来登陆
    username = str(uid)+'@weibo'

    # 判断用户是否已经注册过
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:

        # 注册，并设置特殊的email(user@weibo.com)
        # 设置一个默认的密码，当然，这个密码是没用的，不可以通过输入用户名和密码来登陆
        new_user = User.objects.create_user(username=username,email='user@weibo.com',password=settings.DEFAULT_PASSWORD)
        new_user.is_active = True
        try:
            new_user.save()
        except Exception,e:
            return HttpResponse('连接新浪账号时出错:%s'%e)
        
        # 获取用户的新浪账号
        try:
            sina_profile = client.get.users__show(uid=uid)
        except Exception,e:
            raise ValueError(e)

        # 增加用户档案
        new_prfile = UserProfile(user=new_user)
        new_prfile.screen_name = sina_profile['screen_name'][:10] # 截取前10个字符
        new_prfile.city = '北京'
        new_prfile.introduction = sina_profile['description'][:150]

        # 设置链接信息
        try:
            weibo = Link(user=request.user,type='weibo')
            weibo.name = sina_profile['screen_name']
            weibo.url = 'http://weibo.com/' + sina_profile['profile_url']  
            weibo.save()
        except:
            pass

        try:
            new_prfile.save()
        except Exception,e:
            new_user.delete()
            return HttpResponse('注册账号时服务器出现错误：%s' %str(e))
        else:
            #发送信号
            new_user_register.send(
                sender=new_prfile.user.__class__,
                profile = new_prfile
            )


    # 登录当前的用户
    login_user = authenticate(username=username,password='122126382')
    auth_login(request,login_user)
    return HttpResponseRedirect('/')
