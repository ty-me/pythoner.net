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
import os
import time
from hashlib import md5
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from code.forms import *
from django.contrib import messages
from code.models import *
from django.contrib.auth.decorators import login_required
from settings import ROOT_PATH
import datetime
from signals import new_code_was_post
from django.db.models import Q
from code.models import Code

@cache_page(60)
def list(request,page=1):
    current_page = 'code'
    pre_url = 'code'
    category_name = request.GET.get('category','')
    if category_name:
        suf_url = '?category=%s' %category_name
        page_title   = u'代码分享-{}'.format(category_name)
        try:
            category_obj = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise Http404()
        else:
            code_base_all = Base.objects.filter(display=True,category=category_obj) 
    else:
        page_title   = u'代码分享'
        code_base_all = Base.objects.filter(display=True)
    
    paginator = Paginator(code_base_all, 30)
    try:
        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)
    return render('code_list.html',locals(),context_instance=RequestContext(request))

def list_by_user(request,user_id,page=1):
    categorys = Category.objects.all()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404()
    code_base_all = Base.objects.filter(author=user,display=True)
    paginator = Paginator(code_base_all, 30)
    pre_url = 'code'
    try:
        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)
    return render('code_list.html',locals(),context_instance=RequestContext(request))

def detail(request,code_base_id):
    current_page = 'code'
    next = '/code/%d/' %int(code_base_id)
    try:
        code_base = Base.objects.get(id=code_base_id,display=True)
    except Base.DoesNotExist:
        raise Http404()
    code_base.view()
    codes = Code.objects.filter(base=code_base)
    zips = Zip.objects.filter(base=code_base)
    page_title   = u'{}-代码分享'.format(code_base.title)

    # 记录访问者
    if request.user.is_authenticated() and request.user <> code_base.author:
        visitor,visitor_created = Visitor.objects.get_or_create(base=code_base,user=request.user)
        visitor.sub_time = datetime.datetime.now()
        visitor.save()
        
    return render('code_detail.html',locals(),context_instance=RequestContext(request))

@login_required
@csrf_protect
def add(request):
    current_page = 'code'
    page_title   = u'代码分享'
    code_id = request.GET.get('id',False)
    if code_id:
        page_title = '修改代码基本信息'
    else:
        page_title = '填写代码基本信息'
    try:
        code_base = Base.objects.get(id=code_id,author=request.user)
    except Exception,e:
        code_base = Base()
    """
    填写代码的基本信息
    """
    if request.method == 'GET':
        form = CodeBaseForm(initial={'description':code_base.description},instance=code_base)
        return render('code_add.html',locals(),context_instance=RequestContext(request))

    form = CodeBaseForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        code_base.category = data['category']
        code_base.author = request.user
        code_base.title = data['title']
        code_base.description = data['description']
        code_base.save()

        # 处理模型名
        module_list = data['module'].split(' ')
        for name in module_list:
            try:
                module = Module.objects.get(name=name)
            except Module.DoesNotExist:
                module= Module(name=name)
                module.save()
            code_base.module.add(module)
            messages.success(request,'代码基本信息保存成功！')

        return HttpResponseRedirect('/code/add/%d/' %code_base.id)
    else:
        return render('code_add.html',locals(),context_instance=RequestContext(request))

@login_required
@csrf_protect
def add_by_paste(request,code_base_id):
    current_page = 'code'
    page_title   = u'代码分享'
    try:
        base = Base.objects.get(id=code_base_id,author=request.user)
    except Base.DoesNotExist:
        raise Http404()

    # 如果已经发布过，则是修改代码
    if base.display == True:
        page_title = '修改代码'
        button = '修改代码完毕，马上保存'
    else:
        page_title = '代码分享第2步：粘贴/上传代码'
        button = '添加代码完毕，马上发布'

    # 判断是否是作者本人进入该页面
    if request.user <> base.author:
        raise Http404()

    # 处理GET请求
    if request.method == 'GET':
        form = PasteForm()
        file_form = FileForm()
        codes = Code.objects.filter(base=base)
        zips = Zip.objects.filter(base=base)
        return render('code_add_by.html',locals(),context_instance=RequestContext(request))

    # 处理POST请求
    else:
        languag_id = request.POST.get('language',1)
        content = request.POST.get('content','')

        # 处理分类
        try:
             language = Language.objects.get(id=languag_id)
        except Category.DoesNotExist:
            messages.error(request,"你选择的语言不存在")
            return HttpResponseRedirect('/code/add/%d/' %base.id)

        # 检查代码长度
        if 0 < len(content) <= 20:
            messages.error(request,"代码长度不够20字符")
            return HttpResponseRedirect('/code/add/%d/' %base.id)
        
        try:
            new_code = Code(base=base,language=language,content=content,name='代码片段')
            new_code.save()
        except Exception,e:
            messages.error(request,"保存数据时出现错误")

        return HttpResponseRedirect('/code/add/%d/' %base.id)

@login_required
def add_by_file(request,base_id):
    try:
        base = Base.objects.get(id=base_id,author=request.user)
    except Base.DoesNotExist:
        raise Http404()
    if request.method == 'GET':
        return HttpResponseRedirect('/code/add/%d/' %base.id)
    elif 'file_upload' in request.FILES:
        file = request.FILES['file_upload']
    else:
        messages.warning(request,'请选择文件')
        return HttpResponseRedirect('/code/add/%d/' %base.id)

    #检查文件大小
    file_size = 0
    for chunk in file.chunks():
        file_size += len(chunk)
        if file_size >= 1024*1024*5:
            messages.error(request,'文件大小超过限制')
            return HttpResponseRedirect('/code/add/%d/' %base.id)

    # 处理.py 文件
    lans = Language.objects.filter(~Q(suffix=''))
    code_file_list = [ lan.suffix for lan in lans]
    zip_file_list = ['tar','zip','rar','gz']
    file_suffix        = file.name.split('.')[-1]
    if file_suffix in code_file_list:
        try:
            language = Language.objects.get(suffix=file.name.split('.')[-1])
        except Language.DoesNotExist:
            messages.error(request,'不支持你上传的文件')
            return HttpResponseRedirect('/code/add/%d/' %base.id)
        file.open()
        content = file.read()
        if len(content) < 20:
            messages.error(request,"代码长度少于20字符")
            return HttpResponseRedirect('/code/add/%d/' %base.id)
        code = Code(base=base,content=content,language=language,name=file.name)
        try:
            code.save()
        except Exception,e:
            messages.error(request,'保存代码时，服务器出现错误：'+str(e.message))
        else:
            messages.success(request,'上传python文件成功！')
        return HttpResponseRedirect('/code/add/%d/' %base.id)

    # 处理压缩文件
    elif file_suffix  in zip_file_list:
        base_path = os.path.join(ROOT_PATH,'media/file/')
        md5_key     = md5(u'{}-{}-{}'.format(file.name,time.time(),request.user.id)).hexdigest()
        dir1        = md5_key[0:2]
        dir2        = md5_key[2:4]
        dir3        = md5_key[4:6]
        zip_file_path   = os.path.join(base_path,dir1,dir2,dir3)
        simple_name    = '{}.{}'.format(md5_key,file_suffix)
        if not os.path.exists(zip_file_path):
            os.makedirs(zip_file_path)

        # 判断文件是否存在
        #if os.path.exists(os.path.join(zip_file_path,file.name)):
        #    file.name = str(time.time())+'_'+file.name
        zip_file_name = os.path.join(zip_file_path,simple_name)
        print 'zip_file_name',zip_file_name
        
        try:
            with open(zip_file_name,'wb+') as tmp_file:
                for chunk in file.chunks():
                    tmp_file.write(chunk)
        except Exception,e:
            messages.error(request,'上传文件时服务器出现错误:'+str(e.message))
        else:
            zip = Zip(base=base,path='{}/{}/{}/{}'.format(dir1,dir2,dir3,simple_name),size=int(file.size),name=file.name)
            zip.save()
            messages.success(request,'上传文件成功！')
        return HttpResponseRedirect('/code/add/%d/' %base.id)
    else:
        messages.error(request,'你的文件类型不合法，请上传一下后缀的文件:{}'.\
                format(','.join(code_file_list+zip_file_list)))
        return HttpResponseRedirect('/code/add/%d/' %base.id)

def del_code(request,code_base_id,code_id):
    type = request.GET.get('type',False)
    if not type:
        return HttpResponse("{'status':0,'info':'链接出错'}")
    
    if request.user.is_anonymous():
        return HttpResponse("{'status':0,'info':'你没有登录！'}")

    try:
        code_base = Base.objects.get(id=code_base_id,author=request.user)
    except Base.DoesNotExist:
        return HttpResponse("{'status':0,'info':'你没有权限删除这条记录'}")

    if type == 'code':
        try:
            code = Code.objects.get(id=code_id,base=code_base)
        except Code.DoesNotExist:
            return HttpResponse("{'status':0,'info':'你要删除的记录不存在,或者已经删除'}")
        else:
            code.delete()
    elif type == 'zip':
        try:
            zip = Zip.objects.get(id=code_id,base=code_base)
        except Zip.DoesNotExist:
            return HttpResponse("{'status':0,'info':'你要删除的记录不存在,或者已经删除'}")
        file_path = os.path.join(ROOT_PATH,'media/file')
        file_name = os.path.join(file_path,zip.name)
        zip.delete()
        # return HttpResponse(str(file_name))
        if os.path.exists(file_name):
            os.remove(file_name)
    return HttpResponse("{'status':1,'info':'删除成功'}")

@login_required
def edi_code(request,base_id,code_id):
    try:
        base = Base.objects.get(id=base_id,author=request.user)
    except Base.DoesNotExist:
        raise Http404()
    try:
        code = Code.objects.get(id=code_id,base=base)
    except Code.DoesNotExist:
        raise Http404()
    
    if request.method == 'GET':
        form = PasteForm(initial={'language':code.language,'content':code.content})
        return render('code_edit.html',locals(),context_instance=RequestContext(request))
    form = PasteForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        code.language = data['language']

        if len(data['content']) < 20:
            messages.error(request,'代码长度不够20字符！')
            return HttpResponseRedirect('/code/%s/edit/%s/' %(base.id,code.id))
        else:
            code.content = data['content']

        try:
            code.save()
        except Exception,e:
            messages.error(request,'保存代码时，服务器出现错误'+str(e))
            return HttpResponseRedirect('/code/%s/edit/%s/' %(base.id,code.id))
        else:
            messages.success(request,'修改代码成功！')
            return HttpResponseRedirect('/code/add/%d/' %base.id)
    else:
        return HttpResponseRedirect('/code/%s/edit/%s/' %(base.id,code.id))

@login_required
def publish(request,code_base_id):
    current_page = 'code'
    page_title   = u'代码分享'
    try:
        code_base = Base.objects.get(id=code_base_id,author=request.user)
    except Base.DoesNotExist:
        raise Http404()

    if code_base.code_set.count() < 0 and code_base.zip_set.count() < 0:
        return HttpResponse("你还没有添加任何代码")

    # 判读是发表还是修改
    if not code_base.display:
        # 发送信号
        new_code_was_post.send(
            sender=code_base.__class__,
            code = code_base
        )
    code_base.display = True
    code_base.save()
    return HttpResponseRedirect('/code/%d/' %code_base.id)


@login_required
def delete(request,base_id):
    """
    删除代码
    """
    try:
        code_base = Base.objects.get(id=base_id,author=request.user)
    except Exception,e:
        raise Http404()
    Code.objects.filter(base=code_base).delete() # 删除代码
    zips = Zip.objects.filter(base=code_base)
    for zip in zips:
        file_name = os.path.join(ROOT_PATH,'media','file',zip.name)
        # 删除磁盘上的文件
        if os.path.exists(file_name):
            os.remove(file_name)
        zip.delete() # 删除数据库上的记录
    code_base.delete() # 删除代码信息
    return HttpResponseRedirect('/home/%d/code/' %request.user.id)

def download(request,type,id):
    #########################################################################################
    # 暂时留空
    #########################################################################################
    if type == 'zip':
        return _zip(request,id)
    elif type == 'code':
        pass

def _zip(request,id):
    try:
        zip = Zip.objects.get(id=id)
    except Zip.DoesNotExist:
        return HttpResponse('你要下载的文件不存在，或者已经被删除')

    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login/?next=/code/%d/' %zip.base.id)

    file_path = os.path.join(ROOT_PATH,'media/file')
    try:
        file = open(os.path.join(file_path,zip.path))
    except Exception,e:
        return HttpResponse('读取文件出错')
    else:
        data = file.read()
        file.close()
        zip.download_times += 1
        zip.save()
    response = HttpResponse(data,mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % zip.name
    return response

def _code(request,id):
    pass
