#encoding:utf-8
import os
import time
import threading
import urllib
from hashlib import md5
from BeautifulSoup import BeautifulSoup
from PIL import Image
from models import Tag,Entry
from pythoner.settings import  MEDIA_ROOT,MEDIA_URL
from PIL import Image
import StringIO


class TagingThread(threading.Thread):
    """
    为文章添加标签线程
    """
    def __init__(self,wiki_object):
        self.wiki = wiki_object
        threading.Thread.__init__(self)

    def run(self):
        # 清除已有标签
        print 'start tagging...'
        self.wiki.tag.clear()
        content = u'{0}{1}'.format(self.wiki.title,self.wiki.content)
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

        date = time.strftime('%Y%m%d',time.localtime())
        filepath  = os.path.join(MEDIA_ROOT,'{0}/{1}'.format('wiki',date))
        filedata  = urllib.urlopen(img_url).read()
        print 'filepath',filepath
        
        # make a dir
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        im = Image.open(StringIO.StringIO(filedata))
        filename = os.path.join(filepath,'{0}.jpg'.format(md5(filedata).hexdigest()))
        im.thumbnail((600,600),Image.ANTIALIAS)
        im.convert('RGB').save(filename,'jpeg',quality=100)
        return '{0}wiki/{1}/{2}'.format(MEDIA_URL,date,os.path.basename(filename))


    def run(self):
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
        image_urls = []
        for img in imgs:
            self.title = img[0]
            try:
                remote_url = img[0]
                local_url = img[1]
            except:
                continue
            else:
                image_urls.append(local_url)
                new_html = new_html.replace(remote_url,local_url)

        self.wiki.image_urls = ','.join(image_urls)
        self.wiki.content = new_html
        print 'image saved'
        self.wiki.save()

if __name__ == '__main__':
    html = """ <span style="display: none; ">&nbsp;</span><img alt="\" height="314" src="http://www.php100.com/uploadfile/2012/0301/20120301101756716.jpg" style="text-align: -webkit-center; " width="500" />""" 
    entry = Entry.objects.get(id=1)
    i = ImageThread(entry)
    i.start()
