#encoding:utf-8
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from main.verify.views import *
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from models import Job
import xml
from city import *
from forms import JobForm
from signals import new_job_was_post

def list(request,page=1):
    current_page = 'jobs'
    job_all = Job.objects.filter(display=True).order_by('-sub_time')
    paginator = Paginator(job_all,20)
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
    #########################################################################################
    # 用户操作行为安全保护

    # 计时器
    timer = time.time() - request.session.get('time_stamp',0)

    # 危险操作次数
    action_times = request.session.get('action_times',0)

    # 错误次数是否大于最大
    if action_times >= 1:
        if not check_verify(request):
            return render('verify.html',locals(),context_instance=RequestContext(request))
        else:

            # 重置标志位
            reset(request)
    #########################################################################################
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
            set(request)
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
