#encoding:utf-8
import json
from django.http import HttpResponseBadRequest, HttpResponseNotFound,HttpResponse
from wiki.models import *
from wiki.signals import *

def json_response(dict,request=None):
    """ Return json response
    """
    return HttpResponse(json.dumps(dict), mimetype='application/json; charset=utf-8',status=200)

