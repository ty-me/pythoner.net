#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.NET

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
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from models import Job
import xml
from city import *
from forms import JobForm
from signals import new_job_was_post

def list(request,page=1):
    city         =  request.GET.get('city')
    order        =  request.GET.get('order')
    if order not in ['sub_time','-sub_time','city','-city']:
        order = '-sub_time'

    if city:
        suf_url = u'?city={0}'.format(city)
        job_all      = Job.objects.filter(display=True,city=city).order_by(order)
    else:
        job_all      = Job.objects.filter(display=True).order_by(order)

    paginator    = Paginator(job_all,20)
    current_page = 'jobs'
    pre_url = 'jobs'
    try:
        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)
    return render('jobs_list.html',locals(),context_instance=RequestContext(request))

def detail(request,job_id):
    current_page = 'jobs'
    try:
        job = Job.objects.get(display=True,id=job_id)
    except Job.DoesNotExist:
        raise Http404()
    Job.objects.filter(id=job_id).update(click_times=int(job.click_times+1))
    job.email = str(job.email).replace('@','[at]')
    return render('jobs_detail.html',locals(),context_instance=RequestContext(request))

@csrf_protect
def add(request):
    current_page = 'jobs'

    # 检查用户选择的城市是否存在
    if check_city(request.GET.get('city_name',False)):
        request.session['job_city'] = request.GET.get('city_name')
    else:
        return index(request=request)

    # 打印表单
    if request.method == 'GET':
        form = JobForm()
        return render('jobs_add.html',locals(),context_instance=RequestContext(request))

    # 处理提交数据
    form = JobForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        new_job = Job()
        new_job.title = data['title']
        new_job.city = request.session.get('job_city','北京')
        new_job.company = data['company']
        new_job.website = data['website']
        new_job.email = data['email']
        new_job.content = data['content']
        try:
            new_job.save()
        except Exception,e:
            return HttpResponse('保存招聘信息时出现错误：'+str(e))
        else:
            msg = '提交成功，正在等待管理员审核...'
            # 发送信号
            new_job_was_post.send(
                sender = new_job.__class__,
                job = new_job
            )
        return render('posted.html',locals(),context_instance=RequestContext(request))
    else:
        return render('jobs_add.html',locals(),context_instance=RequestContext(request))

def get_citys():
    # 从xml文件中读取城市列表
    city_xml = open(os.path.join(os.path.normpath(os.path.dirname(__file__)),'city.xml'))
    doc = xml.dom.minidom.parse(city_xml)
    citys = []
    provinces = doc.getElementsByTagName('province')
    for item in provinces:
        entry = {'province':'','citys':[]}
        province = item.getAttribute('name')
        entry['province'] = province
        for city in item.getElementsByTagName('city'):
            city = city.getAttribute('name')
            entry['citys'].append(city)
        citys.append(entry)
    return citys

def check_city(city_name):
    citys = get_citys()
    for entrys in citys:
        for city in entrys['citys']:
            if city == city_name:
                return True
            else:
                continue
    return False
