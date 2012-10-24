#encoding:utf-8
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
