#encoding:utf-8
#file:定时执行任务脚本
import logging
import lxml.html as HTML
from lxml import etree
from browser import BrowserBase
from models import *
import time
import random
connect('test',host='127.0.0.1')

class DoubanGroup(BrowserBase):
    """
    """

    def __init__(self,list_url="http://www.douban.com/group/zhuangb/"):
        self.list_url = list_url
        BrowserBase.__init__(self)
        try:
            html = self.openurl(self.list_url)
        except Exception,e:
            logging.error(e)
        else:
            self.html = html
    
    def get_topic_url(self):
        self.topic_urls  = []
        doc = HTML.document_fromstring(self.html)
        print self.html
        for tr in doc.xpath(".//tr"):
            try:
                a = tr.xpath(".//a")[0]
            except Exception,e:
                print 'error',e
                continue

            title = a.text_content()
            url = a.get('href')
            if url:
                self.topic_urls.append(url)
        return  self.topic_urls
    
    def get_content_info(self,url):
        html = self.openurl(url) 
        doc = HTML.document_fromstring(html)
        title  =  doc.xpath('.//h1')[0].text_content()
        h3 = doc.xpath(".//div[@class='topic-doc']/h3/span")
        datetime = h3[0].text_content()
        a   = h3[1].xpath('.//a')[0]
        author_name = a.text_content()
        author_url =  a.get('href')
        content = doc.xpath(".//div[@class='topic-content']")[0]
        content = etree.tostring(content)
        content = content.replace('<div class="topic-content">','').replace('</div>','')
        comments = self.get_comments_info(doc)

        return {'url':url,'title':title,'content':content,'comments':comments,'datetime':datetime,'author_name':author_name,'author_url':author_url}

    def get_comments_info(self,doc):
        result = []
        comments = doc.xpath(".//div[@class='reply-doc content']")
        for c in comments:
            datetime = c.xpath(".//h4")[0].text_content()[:19]
            a = c.xpath(".//h4/a")[0]
            author_name = a.text_content()
            author_url = a.get('href')
            content = c.xpath(".//p")[0]
            li = {'author_name':author_name,'author_url':author_url,'datetime':datetime,'content':content}
            result.append(li)
        return result

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


if __name__ =='__main__':
    s = DoubanGroup()
    import time
    for url in s.get_topic_url():
        t = DoubanTopic()
        old = DoubanTopic.objects.filter(url=url)
        if len(old):
            print 'old',url
            continue

        print 'total',DoubanTopic.objects.count()
        topic = s.get_content_info(url)

        t.title = topic['title']
        t.url = url
        t.author_name = topic['author_name']
        t.author_url = topic['author_url']
        t.datetime = topic['datetime']
        t.title = topic['title']
        t.content = topic['content']
        t.comments = topic['comments']
        print 'save',t.save()
        print t.title
        print '=='*len(t.title)
        time.sleep(random.randrange(1,3))
