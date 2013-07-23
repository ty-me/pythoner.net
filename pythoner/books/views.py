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

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from main.verify.views import *
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from books.models import *

def list(request,page=1):
    current_page = 'books'
    pre_url = 'books'
    book_all = Book.objects.filter(display=True)
    paginator = Paginator(book_all,20)
    allow_category = True
    try:

        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)

    return render('books_list.html',locals(),context_instance=RequestContext(request))

def detail(request,isbn):
    try:
        book = Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        raise Http404()

    next = "/books/%s/" %book.isbn
    Book.objects.filter(isbn=isbn).update(click_time=book.click_time+1)
    return render('book_detail.html',locals(),context_instance=RequestContext(request))

@csrf_protect
def add(request):
    pass

def edit(request,book_id):
    pass

def delete(request,book_id):
    pass

def category(request,category_id):
    pass
