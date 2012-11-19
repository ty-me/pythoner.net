#encoding:utf-8
from django import template
from books.models import *

register = template.Library()

#获取图书分类
@register.inclusion_tag('books_category.tag.html')
def get_book_category():
    try:
        category_list = Category.objects.all()
    except Category.DoesNotExist:
        category_list = ''
    return {'category_list':category_list}

#获取图书点击排行
@register.inclusion_tag('books_click.tag.html')
def get_book_by_clicktime(count=10): 
    try:
        entry_list = Book.objects.filter(display=True).order_by('-click_time')[0:count]
    except Entry.DoesNotExist:
        entry_list = ''
    return {'entry_list':entry_list}


