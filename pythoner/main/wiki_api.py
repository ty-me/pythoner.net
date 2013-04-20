#encoding:utf-8
import random
import json
from django.http import HttpResponseBadRequest, HttpResponseNotFound,HttpResponse
from wiki.models import *
from wiki.signals import *
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt

def json_response(dict,request=None):
    """ Return json response
    """
    if type(dict) == dict:
        status = dict.get('status')
        info   = dict.get('info')
        if status and not info:
            if status == 2:
                dict['info'] = 'Server error'
            elif status == 3:
                dict['info']  = 'Param error'
            elif status == 4:
                dict['info'] = 'Invalid request'
            elif status == 5:
                dict['info'] = 'Need signin'
    response = HttpResponse(json.dumps(dict), mimetype='application/json; charset=utf-8',status=200)
    return response

@csrf_exempt
def add(request):
    response = {'status':0,'info':''}
    print 'request',request
    if request.method == 'GET':
        response['info'] = 'Invalide method'
        return json_response(response)

    user_id = int(request.REQUEST.get('user',0))
    try:
        cat = request.REQUEST.get('category')
        category = Category.objects.get(name=cat)
    except:
        category = Category.objects.get(name=u'其它python相关')

    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(id=random.randrange(2,10))

    new_wiki          = Entry()
    new_wiki.author   = user
    new_wiki.title    = request.REQUEST.get('title')
    new_wiki.content  = request.REQUEST.get('content')
    new_wiki.category = category
    new_wiki.source   = request.REQUEST.get('source')
    new_wiki.public   = True

    if not new_wiki.title or not new_wiki.content:
        response['status'] = 0
        response['info'] = 'params error'
        return json_response(response)
    try:
        new_wiki.save()
    except Exception,e:
        response['info'] = e.message
        return json_response(response)

    # 发送信号
    new_wiki_was_post.send( sender= new_wiki.__class__,wiki=new_wiki)
    response['status']  = 1
    response['new_wiki_id'] = new_wiki.id
    return json_response(response)

@csrf_exempt
def edit(request):
    if request.method == 'GET':
        return HttpResponseBadRequest('error method')

    response = {'status':0,'info':''}
    wiki_id  = request.REQUEST.get('wiki_id')
    try:
        wiki = Entry.objects.get(id=wiki_id)
    except:
        response['info'] = 'wiki {0} does not exist '.format(wiki_id)
        return json_response(response)

    user_id = int(request.REQUEST.get('user',0))
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except Exception,e:
            response['info'] = e.message
            return json_response(response)
        else:
            wiki.author   = user

    try:
        cat = request.REQUEST.get('category')
        category = Category.objects.get(name=cat)
    except:
        category = Category.objects.get(name='其它python相关')

    
    wiki.title    = request.REQUEST.get('title')
    wiki.content  = request.REQUEST.get('content')
    wiki.category = category
    wiki.source   = request.REQUEST.get('source')

    try:
        wiki.save()
    except Exception,e:
        response['info'] = e.message
        return json_response(response)

    response['status']  = 1
    return json_response(response)
