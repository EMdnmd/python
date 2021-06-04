'''
模板介绍：from验证
coding: utf-8
Team : 无
Author：张恒瑞
Date ：2020/12/31 10:04
Tool ：PyCharm
'''
from django import forms


class  registerfrom(forms.Form):
            user=forms.CharField(max_length=20,min_length=10, required=True,
                            error_messages={
                                    "required":"请输入用户名",
                                    "min_length":"用户名不低于10位",
                                    "max_length":"用户名不大于20位"})


            password=forms.CharField(max_length=30,min_length=10, required=True,
                            error_messages={
                                    "required":"请输入密码",
                                    "min_length":"用户名不低于10位",
                                    "max_length":"用户名不大于30位"})

            pgone=forms.IntegerField(max_value=11,min_value=11,required=True,error_messages={
                  "required": "请输入手机号码",
                  "min_length": "号码不得低于11位",
                  "max_length": "号码不得高于11位"

            })
