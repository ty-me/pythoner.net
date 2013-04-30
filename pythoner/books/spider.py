#encoding=utf-8
import random
import time,math,os,re,urllib,urllib2,cookielib
from BeautifulSoup import BeautifulSoup
import time
import socket
import os
import db
from string import join
from PIL import Image
import os


class BrowserBase(object):
    ERROR = {
        '0':'Can not open the url,checck you net',
        '1':'Creat download dir error',
        '2':'The image links is empty',
        '3':'Download faild',
        '4':'Build soup error,the html is empty',
        '5':'Can not save the image to your disk',
    }
    image_links = []
    image_count = 0

    def __init__(self):
        socket.setdefaulttimeout(20)

    def speak(self,name,content):
        print '[%s]%s' %(name,content)

    def openurl(self,url):
        """
        打开网页
        """
        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

                    ]

        # 随机选取一个agent
        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.google.com')]
        try:
            res = self.opener.open(url)
        except Exception,e:
            self.speak(str(e)+url)
            raise Exception
        else:
            return res


class Spider(BrowserBase):
    name = 'Spider'

    def __init__(self):
        BrowserBase.__init__(self)

        # 开始页地址
        while True:
            #book_page = 'http://book.douban.com/subject/1921890/'
            #book_page = 'http://book.douban.com/subject/4719162/' 
            #book_page = 'http://book.douban.com/subject/3117898/'
            book_page = raw_input('book address:')

            try:
                self.html = self.openurl(book_page).read()
                self.url = book_page
            except Exception,e:
                print e
            else:
                break

    def get_info(self):
        """
        返回图书信息
        """
        book = {}
        soup = BeautifulSoup(self.html)
        book['name'] =  soup.h1.contents[1].string
        info_div = soup.findAll('div',id='info')[0]

        instrution = ''
        span = soup.find('span',{'class':'all hidden'})
        if span:
            for line in span.contents:
                try:
                     line.string
                except AttributeError:
                    continue
                else:
                    instrution += str(line.string)

            book['instrution'] =  instrution.replace('None','<br/>')
        else:
            book['instrution'] = ''



        reg = re.compile(r'(\d{4,8})')
        book['douban_id'] = int(reg.findall(self.url)[0])

        jpg_url =  soup.find('a',{'class':'nbg'})['href']

        for line in str(info_div).split('<br />'):
            #print 'line',line
            soup = BeautifulSoup(line)
            if '作者' in line:
                author = []
                for a in soup.contents[0].findAll('a'):
                    author.append(a.string)
                book['author'] = join(author,'/')

                trans = []

            book['translator'] = ''
            if '译者' in line:
                for a in  soup.contents[0].findAll('a'):
                    trans.append(a.string)
                book['translator'] = join(trans,'/')

            if '出版社' in line:
                book['publish'] =  soup.contents[1].string

            if '出版年' in line:
                book['pub_date'] =  soup.contents[1].string

            if '定价' in line:
                book['price'] = soup.contents[1].string

            if 'ISBN' in line:
                line = str(line)
                reg = re.compile(r'(\d{13})')
                book['isbn'] = int(reg.findall(line)[0])

            if '页数' in line:
                book['pages'] = int(soup.contents[1].string)

        self.download(jpg_url,book['isbn'])
        return book

    def download(self,jpg_url,douban_id):
        """
        下载图片
        """
        root = os.path.normpath(os.path.dirname(__file__))
        file_path = '../static/books/%s.jpeg' %douban_id
        file_path = os.path.join(root,file_path)

        thumb_path = '../static/books/%s_120.jpeg'%douban_id
        thumb_path = os.path.join(root,thumb_path)
        urllib.urlretrieve(jpg_url,file_path)

        # 生成缩略图
        im = Image.open(file_path)
        im.thumbnail((120,120),Image.ANTIALIAS)
        im.save(thumb_path,'jpeg')


if __name__ == '__main__':
    #main()
    s = Spider()
    book = s.get_info()
    #print book
    db.insert_book(book['name'],book['author'],book['translator'],book['publish'],book['pub_date'],book['instrution'],book['price'],book['pages'],book['isbn'],book['douban_id'])

