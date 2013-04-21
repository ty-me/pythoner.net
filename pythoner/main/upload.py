#encoding:utf-8
import os
import time
from hashlib import md5
from PIL import Image
import StringIO
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from utils.common import json_response
import hashlib
from settings import MEDIA_ROOT,DOMAIN,MEDIA_URL
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def general_file_upload_handle(request):
    response = {'error':1,'message':0,'url':'','size':''}
    if request.method == 'GET':
        response['message'] = 'POST request only'
        return json_response(response)

    if 'imgFile' not in request.FILES:
        response['error'] = 1
        response['message'] = 'File name error' + str(request.FILES.keys())
        return json_response(response)

    else:
        file_type = request.POST.get('file_type','unknow')
        dir       = request.POST.get('dir','images')
        print 'request.get',request.GET
        try:
            return _general_file_upload_handle(request.FILES['imgFile'],file_type,dir)
        except Exception,e:
            import traceback
            response['message'] = traceback.print_exc()
            return json_response(response)

@csrf_exempt
def _general_file_upload_handle(file,file_type,dir):
    response = {'error':0,'message':0,'url':'','size':''}
    date_str  = time.strftime('%Y%m%d',time.localtime())
    filepath  = os.path.join(MEDIA_ROOT,'{0}/{1}'.format(dir,date_str))
    file.name = str(time.time())+'-'+file.name
    filedata  = file.read()
    filename  = os.path.join(filepath,file.name)
    
    # make a dir
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    print 'file type',file_type
    if file_type == 'image':
        im = Image.open(StringIO.StringIO(filedata))
        filename = os.path.join(filepath,'{0}.jpg'.format(md5(filedata).hexdigest()))
        im.thumbnail((600,600),Image.ANTIALIAS)
        im.convert('RGB').save(filename,'jpeg',quality=100)

    else:
        f = open(filename,'wb')
        f.write(filedata)
        f.close()

    response['error'] = 0
    response['url'] = filename.replace(MEDIA_ROOT,os.path.join(DOMAIN,MEDIA_URL))
    return json_response(response)
