#encoding:utf-8
from wiki_threads import *
from signals import *

def deal_with_new_wiki(sender,**kwargs):
    """ send a message to admin's account """
    # 开启线程添加文章标签
    new_wiki = kwargs.get('wiki')
    TagingThread(wiki_object=new_wiki).start()
    # 开启下载图片的线程
    ImageThread(new_wiki).start()

new_wiki_was_post.connect(deal_with_new_wiki)
