#encoding:utf-8
from django import template
register = template.Library()

@register.filter()
def trans_app(app_name):
    app = {'Auth':'权限系统',
           'Comments':'评论系统',
           'News':'新闻模块',
           'Wiki':'维基模块',
           'Topic':'讨论模块',
           'Code':'代码模块',
           'Jobs':'招聘模块',
           'Sites':'站点管理',
           'Pm':'短信模块',
           'Books':'图书模块',
           'Link':'链接模块',
           'Spider':'站点爬虫',
           'Home':'用户中心',}
    try:
        new_app = app[app_name]
    except KeyError:
        new_app = app_name
    return new_app

