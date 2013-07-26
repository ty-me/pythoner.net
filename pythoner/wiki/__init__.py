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

    #向管理员发站内信提醒
    content = "http://pythoner.net/admin/wiki/entry/{}/".format(new_wiki.id)
    from pm.models import Pm
    from accounts.models import User
    if new_wiki.author.id <> 1:
        Pm(
            from_user = User.objects.get(id=1),
            to_user = User.objects.get(id=1),
            title='新的文章等待审核:{}'.format(new_wiki.title),
            content=content,
            system = True
        ).save()
    

new_wiki_was_post.connect(deal_with_new_wiki)
