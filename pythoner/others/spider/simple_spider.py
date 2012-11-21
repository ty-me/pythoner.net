#encoding:utf-8
#file:定时执行任务脚本
import logging
import sys
import random
from string import join
import sys
sys.path.insert(0,'/www/pythoner')
import threading
import settings
from django.core.management import setup_environ
setup_environ(settings)
from main.email.views import send_email
from django.contrib.auth.models import User
from wiki.models import *
from jobs.models import *
from wiki.image_downloader import ImageDownloader
from wiki.views import TagingThread
import datetime
import time
import math
from BeautifulSoup import BeautifulSoup
from browser import BrowserBase
import threading

class SibSpider(BrowserBase):
    """
    抓取simple-is-better.com招聘的信息
    """

    def __init__(self,list_url="http://simple-is-better.com/jobs/"):
        self.list_url = list_url
        BrowserBase.__init__(self)
        try:
            html = self.openurl(self.list_url)
        except Exception,e:
            self.logger.error(e)
        else:
            self.html = html
            self.soup = BeautifulSoup(self.html)

    def get_job_url(self,html=False):
        item_links  = []
        main_soup = self.soup.find('div',{'class':'main_content'})
        for div in main_soup.findAll('div',{'class':'job'}):
            href = div.h2.findAll('a')[1]['href']
            url = self._formate_url(href)
            item_links.append(url)

        return item_links[:5]

    def _formate_url(self,href):
        url = "http://simple-is-better.com%s" %href
        return url

    def get_job_info(self,url=""):
        try:
            html = self.openurl(url)
        except Exception,e:
            print e,url
            return
        soup = BeautifulSoup(html)
        data = {}
        s = soup.find('h1').string
        data['title'] = '招聘' + str(s)

        s = str(soup.find('h3').contents[0])
        data['city'] = s.split('python')[0].replace(' ','')

        p = soup.find('div',{'class':'meta box'}).findAll('p')
        try:
            data['company'] = p[0].contents[1].replace(' ','').replace('(','')
            data['website'] = p[1].a['href']
            data['email'] =  p[2].a.string.replace('(#)','@').replace(' ','')
        except Exception,e:
            # 信息不全
            print '信息不全，跳过',url
            return False

        s = str(soup.find('div',{'class':'content box'}))
        s = s.replace('<div class="content box">','').replace('</div>','')
        data['content'] = s

        return data

    def get_wiki_url(self,url="http://simple-is-better.com/news/"):
        html = self.openurl(url)
        soup = BeautifulSoup(html)
        urls = []
        for h2 in soup.find('div',{'class':'main_content'}).findAll('h2'):
            href = h2.a['href']
            url = self._formate_url(href)
            urls.append(url)
        return urls

    def get_wiki_info(self,url="http://simple-is-better.com/news/815"):
        html = self.openurl(url)
        soup = BeautifulSoup(html)
        data = {}

        data['source'] = url
        data['public'] = True
        for p in  soup.find('div',{'class':'meta box'}).findAll('p'):
            if '原始出处' in str(p):
                data['source'] = p.a['href']
                break


        category = soup.find('div',{'class':'nav box'}).findAll('a')[2].string.replace(' ','')
        categorys = [
            ('技术聚会',5),
            ('系统架构',7),
            ('GAE',10),
            ('Django',9),
            ('Tornado',9),
            ('Twisted',9),
            ('创业故事',10),
        ]


        data['category'] = Category.objects.get(id=10)
        for c in categorys:
            if c[0] == category:
                data['category'] = Category.objects.get(id=c[1])
                break

        data['title'] =  soup.find('h1').string
        user_id = 15
        data['author'] = User.objects.get(id=user_id)
        s = soup.find('div',{'class':'content box'}).find('div',{'class':'box'})
        s = str(s).replace('<div class="box">','').replace('</div>','')
        data['content'] = s

        return data

def update_job(display=True):
    i = SibSpider()
    url_list = i.get_job_url()

    while len(url_list):
        url = url_list.pop(-1)
        data = i.get_job_info(url)

        # 如果抓取到的数据不正确，则跳过
        if not data:
            continue

        try:
            Job.objects.get(email=data['email'])
        except Job.DoesNotExist:
            pass
        else:
            continue

        new_job = Job()
        new_job.title = data['title']
        new_job.city = data['city']
        new_job.company = data['company']
        new_job.website = data['website']
        new_job.email = data['email']
        new_job.content = data['content']
        new_job.display = display
        new_job.click_times = random.randrange(2,30)
        new_job.save()
        if not new_job.id:
            url_list.insert(0,url)
        else:
            print data['title']

def update_wiki(url='http://simple-is-better.com/news/?page=1'):
    s = SibSpider()
    url_list = s.get_wiki_url(url)

    # 检查页面是否有更新
    url = url_list[0]
    data = s.get_wiki_info(url)
    try:
        Entry.objects.get(source=data['source'])
    except Entry.DoesNotExist:
        pass
    except KeyError:
        pass
    else:
        print '木有新的文章可以抓取'
        return

    try:
        Entry.objects.get(title=data['title'])
    except Entry.DoesNotExist:
        pass
    except KeyError:
        pass
    else:
        print '木有新的文章可以抓取'
        return

    for url in url_list:
        url = url_list.pop(-1)
        data = s.get_wiki_info(url)

        try:
            Entry.objects.get(source=data['source'])
        except Entry.DoesNotExist:
            pass
        else:
            print '跳过重复的内容'
            continue

        new_wiki = Entry()
        new_wiki.category = data['category']
        new_wiki.title = data['title']
        new_wiki.content = data['content']
        new_wiki.source = data['source']
        new_wiki.author = data['author']
        new_wiki.public = data['public']
        new_wiki.click_time = random.randrange(3,50)
        try:
            new_wiki.save()
        except Exception,e:
            print e
            continue

        if new_wiki.id:
            print new_wiki.title
            print '==' * len(wiki.title)
            TagingThread(new_wiki).run()
            ImageDownloader(new_wiki).run()
        else:
            print 'fuck error '


if __name__ == '__main__':
    while 1:
        update_wiki()
    	update_job()
        time.sleep(60*15)
