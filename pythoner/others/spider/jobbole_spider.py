#encoding:utf-8
#file:定时执行任务脚本
import logging
import sys
import random
import sys
sys.path.insert(0,'/www/pythoner')
sys.path.insert(0,'/Users/tianyu/Dev/pythoner')

from string import join
import threading
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.email.views import send_email
from django.contrib.auth.models import User
from wiki.models import *
import datetime
import time
import math
import lxml.html as HTML
from lxml import etree
from browser import BrowserBase
from wiki.image_downloader import ImageDownloader
from wiki.views import TagingThread

class JobboleSpider(BrowserBase):
    """
    """

    def __init__(self,list_url="http://blog.jobbole.com/?s=python&x=0&y=0"):
        self.list_url = list_url
        BrowserBase.__init__(self)
        try:
            html = self.openurl(self.list_url)
        except Exception,e:
            logging.error(e)
        else:
            self.html = html

    def get_blogs_url(self):
        links = []
        doc = HTML.document_fromstring(self.html)
        for h2 in doc.xpath(".//h2"):
            try:
                href = h2.xpath(".//a")[0].get('href')
            except :
                pass
            else:
                links.append(href)
        return links[:2]

    def get_blog_info(self,url="http://blog.jobbole.com/16141/"):
        html = self.openurl(url)
        doc = HTML.document_fromstring(html)
        data = {}
        data['title'] = doc.xpath('//h1')[0].text_content()
        if '伯乐周刊' in data['title']:
            return False

        data['source'] = url
        content =  doc.xpath("//div[@class='entry-content']")[0]
        content = etree.tostring(content)
        #print content
        content = content.replace('<div class="entry-content">&#13;','').replace('<div style=" margin:5px 0 5px 5px; float:right;">','')
        content = content.replace('<div class="textwidget"/>','').replace('</div>','')
        data['content'] = content
        data['author'] = User.objects.get(id=19)
        data['category'] = Category.objects.get(id=10)
        return data

def update_blogs():
    i = JobboleSpider()
    url_list = i.get_blogs_url()
    while len(url_list):
        url = url_list.pop(-1)
        try:
            data = i.get_blog_info(url)
        except Exception,e:
            print e,url
            continue
        if not data:
            continue


        try:
            Entry.objects.get(title=data['title'])
        except Entry.DoesNotExist:
            pass
        except Exception:
            continue
        else:
            continue

        try:
            Entry.objects.get(source=data['source'])
        except Entry.DoesNotExist:
            pass
        except Exception:
            continue
        else:
            continue


        try:
            Entry.objects.get(content=data['content'])
        except Entry.DoesNotExist:
            pass
        except Exception:
            continue
        else:
            continue

        new_wiki = Entry()
        new_wiki.category = data['category']
        new_wiki.title = data['title']
        new_wiki.content = data['content']
        new_wiki.source = data['source']
        new_wiki.author = data['author']
        new_wiki.public = True
        new_wiki.click_time = random.randrange(1,40)
        new_wiki.save()
        if new_wiki.id:
            print new_wiki.title
            TagingThread(new_wiki).run()
            ImageDownloader(new_wiki).run()
        else:
            print 'fuck'

if __name__ =='__main__':
    while True:
        time.sleep(1)
        try:
            update_blogs()
        except Exception,e:
            print 'error at ',e

        time.sleep(5*60)
