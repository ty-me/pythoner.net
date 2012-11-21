#encoding:utf-8
from mongoengine import *

class Post(Document):
    url = StringField(max_length=150,required=True)
    author_name  = StringField(max_length=120,required=True)
    author_url = StringField()
    datetime = StringField(max_length=20)
    title = StringField(max_length=500,required=True)
    content = StringField()

class DoubanTopic(Post):
    comments = ListField()
