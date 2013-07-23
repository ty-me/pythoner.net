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

import xml.dom.minidom
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.contrib.auth.decorators import login_required
from main.verify.views import *
import os

def get_citys():
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

def index(request):
    current_page = 'jobs'
    """
    所在城市列表
    """
    if 'city_name' in request.GET:
        if check_city(request.GET.get('city_name')):
            request.session['job_session'] = request.GET.get('city_name')
            return HttpResponseRedirect('/jobs/add/')
        else:
            return HttpResponse('你所选择的城市不存在，请检查！')
    citys = get_citys()
    return render('jobs_city.html',locals(),context_instance=RequestContext(request))


