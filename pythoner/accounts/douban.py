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

from douban_client import DoubanClient
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from models import UserProfile
from models import Link
from accounts.signals import new_user_register
import settings


API_KEY = settings.DOUBAN_API_KEY
API_SECRET = settings.DOUBAN_API_SECRET
SCOPE = settings.DOUBAN_SCOPE
CALLBACK_URL = settings.DOUBAN_CALLBACK_URL

client = DoubanClient(API_KEY, API_SECRET, CALLBACK_URL)

def index(request):
    """
    跳转到验证页面
    """
    auth_url = client.authorize_url 
    return HttpResponseRedirect(auth_url)

def callback(request):
    """
    用户授权后的回调
    """
    code = request.GET.get(u'code')
    client.auth_with_code(code) 
    me = client.user.me
    username = '%s@douban' %me['id']
    # 不保存用户的token,因为不会在其它地方操作用户数据

    # 判断用户是否已经注册过
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:

        # 注册，并设置特殊的email(user@weibo.com)以此判断是微波用户
        new_user = User.objects.create_user(username=username,email='user@douban.com',password=settings.DEFAULT_PASSWORD)
        new_user.is_active = True
        try:
            new_user.save()
        except Exception,e:
            return HttpResponse('连接豆瓣账号时出错:%s'%e)

        # 增加用户档案
        new_prfile = UserProfile(user = new_user)
        new_prfile.screen_name = me['name'][:10] # 截取前10个字符
        new_prfile.city = me['loc_name']
        new_prfile.introduction = me['desc'][:200]

        # 设置链接信息
        if True:
            douban = Link(user=new_user,type='douban')
            douban.name = me['name']
            douban.url = me['alt']
            douban.save()

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

        # 在微波上关注本站
        #try:
        #    api.create_friendship(user_id=1896993041)
        #except :
        #    pass

    # 登录当前的用户
    login_user = authenticate(username=username,password='122126382')
    auth_login(request,login_user)
    return HttpResponseRedirect('/')
