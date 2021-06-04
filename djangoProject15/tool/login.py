'''
模板介绍：
coding: utf-8
Team : 无
Author：张恒瑞
Date ：2021/1/4 7:49
Tool ：PyCharm
'''
import sys

from  django.shortcuts import  render ,HttpResponse,redirect
from  django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response


class   login(MiddlewareMixin):
    # def process_request(self,request):
    #             user=request.session.get("userid")
    #             if user:
    #                 print(user)
    #                 return None
    #             elif request.path not in ["/login/"]:
    #                 print(user)
    #                 return   redirect("APP1:login")
    def  process_response(self,request,response):
        return  response

    def reocess_exception(self,request,exception):
            print(exception)
            ip=request.META.get("REMOTE_ADDR")
            if ip =="127.0.0.1":
                return technical_500_response(request, *sys.exc_info())
            return  redirect("APP1:login")
