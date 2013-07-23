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

import time
import re
from DjangoVerifyCode import Code
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
from django import http

try:
    import settings
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

class PreventWatering(object):
    """
    防灌水
    """

    verify_code_uri   = '/verify/code/'
    verify_check_uri  = '/oh-my-god/check/'
    verify_page_uri   = '/oh-my-god/'
    expaths            = ['/upload/']

    def process_request(self,request):
        if request.path == self.verify_code_uri:
            code =  Code(request)
            code.type = 'number'
            return code.display()

        elif request.path == self.verify_page_uri:
            return render('verify.html',locals(),context_instance=RequestContext(request))

        elif request.path == self.verify_check_uri:
            code = Code(request)
            _code = request.REQUEST.get('verify','')
            print 'request',request.REQUEST

            # 检查用户输入的验证码是否正确
            if not code.check(_code):
                next = self.verify_page_uri
            else:
                request.session['post_times'] = 0
                request.session['post_stamp'] = time.time()
                next = request.session.get('next','/')
            return HttpResponseRedirect(next)
        
        if not request.path in self.expaths:
            timer = time.time() - request.session.get('post_stamp',0)
            post_times = request.session.get('post_times',0)
            # 提交次数是否大于单位时间的最大值
            if request.method == 'POST':
                if post_times >= 3:
                    request.session['next'] = request.META.get('HTTP_REFERER','/')
                    return HttpResponseRedirect(self.verify_page_uri)

                elif timer >= 60:
                    request.session['post_times'] = 0
                    request.session['post_stamp'] = time.time()
                
                request.session['post_times'] = request.session['post_times']+1
                request.session.save()

class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
        
        
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
        """
    def process_request(self, request):
        
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
            
            return response
        
        return None
    
    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
        
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        
        return response

