#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.NET

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
