'''
模板介绍：
coding: utf-8
Team : 无
Author：张恒瑞
Date ：2021/1/5 8:16
Tool ：PyCharm
'''
import re

from    rest_framework import  serializers


# class  Bookserializers(serializers.Serializer):
#     id=serializers.IntegerField()
#     bookname=serializers.CharField(max_length=100)
#     bookauthor=serializers.CharField(max_length=20)
#     bookprice=serializers.FloatField(min_value=0)
#     bookpublic=serializers.CharField(max_length=20)


# 通过模型生成序列化器
from APP1.models import Book


class  Bookserializers(serializers.ModelSerializer):
        class Meta:
            model=Book
            fields=['bookname','bookauthor','bookpublic','bookprice']
            # fields="__all__"d
        #         单子段验证
        def validated_bread(self,value):
            print(value,type(value),"akan")
            return  value
        # 多字段验证
        def validate(self, attrs):
            print(attrs)
            if re.search(r"反政府",attrs["bookname"]):
                raise   serializers.ValidationError("书名不正确")
            return   attrs