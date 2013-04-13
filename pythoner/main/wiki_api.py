#encoding:utf-8
import random
import json
from django.http import HttpResponseBadRequest, HttpResponseNotFound,HttpResponse
from wiki.models import Entry
from wiki.signals import *
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add(request):
    if request.method == 'GET':
        HttpResponseBadRequest('error method')

    if request.META['REMOTE_ADDR'] <> '127.0.0.1':
        HttpResponseBadRequest('error')

    response = {'status':0,'info':''}

    user_id = int(request.REQUEST.get('user',0))
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(id=random.randrange(1,2))

    new_wiki         = Entry()
    new_wiki.author  = user
    new_wiki.title   = request.REQUEST.get('title')
    new_wiki.content = request.REQUEST.get('content')
    new_wiki.content += """ <span style="display: none; ">&nbsp;</span><img alt="\" height="314" src="http://www.php100.com/uploadfile/2012/0301/20120301101756716.jpg" style="text-align: -webkit-center; " width="500" />""" 

    new_wiki.source  = request.REQUEST.get('source')
    new_wiki.public  = True
    if not new_wiki.title or not new_wiki.content:
        response['status'] = 0
        response['info'] = 'params error'
        return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)

    try:
        new_wiki.save()
    except Exception,e:
        response['info'] = e.message
        return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)

    # 发送信号
    new_wiki_was_post.send( sender= new_wiki.__class__,wiki=new_wiki)
    
    response['status']  = 1
    response['new_wiki_id'] = new_wiki.id
    print new_wiki.title
    print response
    return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)


