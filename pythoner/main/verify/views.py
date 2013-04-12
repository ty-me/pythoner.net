#encoding:utf-8
from django.http import HttpResponse
import Image,ImageDraw,ImageFont,random,StringIO
import time,os
from DjangoVerifyCode import Code


def display(request):
    code =  Code(request)
    code.words = ['hello','world','helloworld']
    #code.type = 'world'
    code.type = 'number'
    return code.display()


