from django.shortcuts import render
from django.views import View
from rest_framework import serializers, response
# Create your views here.

from  rest_framework.generics import  GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from APP1.models import Book
from APP2.serializerss import Bookserializers


class   BOOKINFO(GenericAPIView):
            queryset =Book.objects.all()
            def get(self,request,bid=-1):
                print(bid)
                if   bid<0:
                    return  self.find_many(request)
                else:
                    return  self.find_one(request,bid)


            def find_many(self,request):
                bs=Bookserializers(instance=self.queryset.all(),many=True)
                print(bs.data)
                return  Response(data=bs.data)

            def find_one(self,request,bid):
                book=self.queryset.get(id=bid)
                bs=Bookserializers(instance=book)
                print(bs.data)
                return  Response(data=bs.data)


class addbooks(APIView):
    # queryset = Book.objects.all()
    serializer_class=Bookserializers
    def  post(self,request):
        print("aa")
        print(request.POST.dict())
        bs=Bookserializers(data=request.data)
        if bs.is_valid():
             print(bs.validated_data)
             bs.save()
             return Response({"code": 1,"mgs":"添加成功"})
        else:
             print(bs.errors)
             return Response({"code": 0,"msg":bs.errors})