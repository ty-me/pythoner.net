#encoding:utf-8
import threading
import time,math,os,re,urllib,urllib2,cookielib
from BeautifulSoup import BeautifulSoup
import time
import os
from PIL import Image
from models import *

class TagingThread(threading.Thread):
    """
    为文章添加标签线程
    """
    def __init__(self,wiki_object):
        self.wiki = wiki_object
        threading.Thread.__init__(self)

    def run(self):
        # 清除已有标签
        self.wiki.tag.clear()

        content = str(self.wiki.title) + self.wiki.content
        for tag in Tag.objects.all():
            if content.lower().count(tag.name.lower()) > 0:
                self.wiki.tag.add(tag)

        self.wiki.save()

    def test(self):
        try:
            self.run()
        except Exception,e:
            return e
        else:
            return 'OK'


class ImageThread(threading.Thread):

    def __init__(self,wiki):
        self.html = wiki.content
        self.wiki = wiki        # wiki models object
        threading.Thread.__init__(self)

    def get_new_url(self,img_url):
        """
        将图片下载，并返回一个本地路径
        """
        if img_url.startswith('..'):
            img_url = img_url.replace('..','').replace('//','')
            img_url = os.path.join('/',img_url)

        name = 'wiki_%s_%s' %(self.wiki.id,time.time())
        date = time.strftime('%Y%m%d',time.localtime())
        dir_name =  '/var/pythoner.net/static/upload/%s/' %date
        if not os.path.isdir(dir_name):
            try:
                os.makedirs(dir_name)
            except Exception,e:
                print e,dir_name
                return False
        file_name = os.path.join(dir_name,'%s.jpg'%name)
        print file_name

        try:
            urllib.urlretrieve(img_url,file_name)
        except Exception,e:
            print e
            return img_url
        else:
            return '/static/upload/%s/%s.jpg' %(date,name)

    def run(self):
        #self.wiki.title = 'fuck title'
        print 'start download img...'
        soup = BeautifulSoup(self.html)
        img_soup = soup.findAll('img')
        if not img_soup:
            return

        imgs = []
        for img in img_soup:
            try:
                remote_url = img['src']
            except Exception,e:
                continue

            local_url = self.get_new_url(remote_url)
            if not local_url:
                continue
            else:
                li = (remote_url,local_url)
                imgs.append(li)
        new_html = self.html
        print imgs
        for img in imgs:
            self.title = img[0]
            try:
                remote_url = img[0]
                local_url = img[1]
            except:
                continue
            else:
                new_html = new_html.replace(remote_url,local_url)

        self.wiki.content = new_html
        print 'image saved'
        self.wiki.save()

if __name__ == '__main__':
    html = """ <span style="display: none; ">&nbsp;</span><img alt="\" height="314" src="http://www.php100.com/uploadfile/2012/0301/20120301101756716.jpg" style="text-align: -webkit-center; " width="500" />""" 
    entry = Entry.objects.get(id=1)
    s = ImageDownloader(entry)
    s.run()
