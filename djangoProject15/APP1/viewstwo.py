from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView
from APP1.models import Book, Bookfigure, user
from django.core.paginator import Paginator
'''
模板介绍：
coding: utf-8
Team : 无
Author：张恒瑞
Date ：2020/12/30 19:27
Tool ：PyCharm
'''
class buy_books(View):
        def get(self,request):
                books=Book.objects.all()
                sk=Bookfigure.objects.filter()
                print(sk)
                return  render(request,"add_author.html",locals())
        def post(self,request):
                book=request.POST.dict()
                book.pop("csrfmiddlewaretoken")
                print(book)
                books=Book.objects.get(pk=book["book_id"])
                userid = request.session.get('userid')
                print(userid)
                users=user.objects.get(pk=3)
                print(users)
                Bookfigure.objects.create(user=users,book=books)
                return redirect("APP1:butybooklist")
                # return  HttpResponse("进来了")
class listbuybook(ListView):
                template_name = "author_list.html"
                paginate_by = 4
                # paginate_orphans = 1
                context_object_name = "books"
                page_kwarg = "fall"
                model =Bookfigure


class  listsheet(ListView):
        def get(self,request,pall,fall=1):
                sk=Bookfigure.objects.filter(user=pall)
                title = ""
                pages =""
                for i in sk:
                    title = i.user.name
                    pages=i.user.di
                    print(pages)

                pagi=Paginator(sk,4)
                page=request.GET.get("page",fall)
                item=pagi.page(page)
                return  render(request,"consumption_list.html",locals())
