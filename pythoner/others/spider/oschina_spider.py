#encoding:utf-8
#file:定时执行任务脚本
import logging
import sys
sys.path.insert(0,'/www/pythoner')

import random
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
from BeautifulSoup import BeautifulSoup
from browser import BrowserBase
from wiki.image_downloader import ImageDownloader
from wiki.views import TagingThread

class OschinaSpider(BrowserBase):
    """
    """

    def __init__(self,list_url="http://www.oschina.net/search?q=python&scope=news"):
        self.list_url = list_url
        BrowserBase.__init__(self)
        try:
            html = self.openurl(self.list_url)
        except Exception,e:
            logging.error(e)
        else:
            self.html = html

    def get_wiki_url(self,html=False):
        soup = BeautifulSoup(self.html)
        item_links  = []
        for h3 in soup.findAll('h3'):
            href = h3.find('a')['href']
            url = self._formate_url(href)
            item_links.append(url)

        return item_links[:4]

    def _formate_url(self,href):
        if 'http://' in href:
            return href
        url = "http://www.oschina.net%s" %href
        return url

    def get_wiki_info(self,url=""):
        html = self.openurl(url)
        soup = BeautifulSoup(html)
        data = {}
        data['title'] = soup.find('h1').text
        data['source'] = url
        content = ''
        info = False 
        # 其详细页面的布局多有不同，因此要根据实际清空区分解析
        info1 = soup.find('div',{'class':'Body NewsContent TextContent NewsType1'})
        info2 = soup.find('div',{'class':'detail'})
        info3 = soup.find('div',{'class':'Body NewsContent TextContent NewsType2'})

        if info1 or info3:
            info = info1 or info3
            for line in info.contents[9:]:
                html = str(line)
                content += html
        
        elif info2:
            info = info2
            for line in info.contents:
                html = str(line)
                content += html

        if not content or not info:
            raise ValueError('没有找到文章内容url:%s' %url)
            return False

        content = content.replace('<p>&nbsp;</p>','')
        # 找到文章中无用的icon替换
        for img in info.findAll('img'):
            if '/img/logo/' in img['src']:
                s = str(img)
                content = content.replace(s,'')
        dump = soup.find('p',{'class':'ProjectOfNews'})
        if dump:
            s = str(dump)
            content = content.replace(s,'')

        data['content'] = content

        user_id = 20
        data['author'] = User.objects.get(id=user_id)
        data['category'] = Category.objects.get(id=5)
        return data
def update_wiki():
    i = OschinaSpider()
    url_list = i.get_wiki_url()
    while len(url_list):
        url = url_list.pop(-1)
        data = i.get_wiki_info(url)

        try:
            Entry.objects.get(source=data['source'])
        except Entry.DoesNotExist:
            print 'new url',url
            pass
        except Exception:
            continue
        else:
            continue

        try:
            Entry.objects.get(title=data['title'])
        except Entry.DoesNotExist:
            print 'new url',url
            pass
        except Exception:
            continue
        else:
            continue

        try:
            Entry.objects.get(title=data['title'])
        except Entry.DoesNotExist:
            print 'new url',url
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
        new_wiki.click_time = random.randrange(1,20)
        new_wiki.save()
        if new_wiki.id:
            print new_wiki.title
            print '=='*len(new_wiki.title)
            TagingThread(new_wiki).run()
            ImageDownloader(new_wiki).run()
        else:
            print 'fuck'

if __name__ == '__main__':
    while 1:
        time.sleep(2)
        try:
            update_wiki()
        except Exception,e:
            print 'error at ',e
        else:
            time.sleep(5*60)
