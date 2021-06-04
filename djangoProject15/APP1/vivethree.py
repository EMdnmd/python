'''
模板介绍：登录 设置  注册 退出
coding: utf-8
Team : 无
Author：张恒瑞
Date ：2020/12/31 9:55
Tool ：PyCharm
'''
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView
from APP1.models import Book, Bookfigure, user
from django.core.paginator import Paginator
#注册
class  register(View):
    def get(self,request):
          return  render(request,"register.html")
    def post(self,request):
            userdict=request.POST.dict()

            userdict.pop("csrfmiddlewaretoken")
            if userdict["password"]==userdict["passwords"]:
                   try:
                        userdict.pop("passwords")
                        user.objects.create(**userdict)

                        return redirect("APP1:listbook")
                   except Exception as  ex:
                            print(ex)
                            return  HttpResponse("输入报错请重新输入")
            else:
                    ex="密码输入不正确"
                    return  render(request,"register.html",locals())


#登录
class login(View):
        def get(self,request):

             return  render(request,"login.html")
        def post(self,request):
            userdict=request.POST.dict()
            userdict.pop("csrfmiddlewaretoken")
            users=user.objects.get(**userdict)
            if users :
                        userer=users.di
                        request.session["userid"]=userer
            else:
                    print("没进来")
            return  render(request,"register.html")

#退出
class exits(View):
       def get(self,request):
            del  request.session["userid"]
            return  render(request,"login.html")
