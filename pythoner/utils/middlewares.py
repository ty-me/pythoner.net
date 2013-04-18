#encoding:utf-8
import time 
from DjangoVerifyCode import Code
from django.shortcuts import render_to_response as render
from django.template import RequestContext

class PreventWatering(object):
    """
    防灌水
    """

    def process_request(self,request):
        if request.method == 'GET':
            pass

        with_out = ['/main/verify/','/','/wiki/','/topic/','/books/','/jobs/','/code/']
        with_out = ['/main/verify/']
        for path in with_out:
            if request.path.endswith(path):
                return

        timer = time.time() - request.session.get('post_stamp',0)
        post_times = request.session.get('post_times',0)

        # 提交次数是否大于单位时间的最大值
        if request.method == 'POST':
            if post_times >= 3:
                _code = request.REQUEST.get('verify','') 
                code = Code(request)

                # 检查用户输入的验证码是否正确
                if not code.check(_code):
                    return render('verify.html',locals(),context_instance=RequestContext(request))
                else:
                    request.session['post_times'] = 0
                    request.session['post_stamp'] = time.time()

            elif timer >= 60:
                request.session['post_times'] = 0
                request.session['post_stamp'] = time.time()
            
            request.session['post_times'] = request.session['post_times']+1
            request.session.save()






import re

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

