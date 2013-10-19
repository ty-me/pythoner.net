#encoding:utf-8
from django import template
register = template.Library()

@register.filter()
def trans_app(app_name):
    app = {'Auth':'权限系统',
           'Comments':'评论系统',
           'News':'新闻',
           'Wiki':'维基',
           'Topic':'讨论',
           'Code':'代码',
           'Jobs':'招聘',
           'Sites':'站点管理',
           'Pm':'短信',
           'Books':'图书模块',
           'Link':'酷站',
           'Spider':'站点爬虫',
           'Home':'用户中心',}
    try:
        new_app = app[app_name]
    except KeyError:
        new_app = app_name
    return new_app

