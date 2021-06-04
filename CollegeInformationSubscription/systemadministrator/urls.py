"""CollegeInformationSubscription URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from systemadministrator import views

app_name = "Administrator"
urlpatterns = [
    # 管理员页面
    path("", views.index, name="index"),
    #  用户信息分页路由
    path("studentslist/<int:pall>", views.studentslist, name="studentslist"),
    # 用户信息
    path("studentslist/", views.studentslist, name="studentslist"),
    # 用户删除路由
    path("deletes/<int:id>/", views.delets, name="deletes"),
    # 主信息
    path("home/", views.home, name="home"),
    path("studentsadd/", views.addstudents, name="studentsadd"),
    # 更改学生密码
    path("studentsup/<int:id>", views.updatastudents, name="studentsup"),
    # 添加数据
    path("addbook/", views.addbook, name="addbook"),
    # 书籍列表
    path("booklist/", views.booklist, name="booklist"),
    path("booklist/<int:pall>", views.booklist, name="booklist"),
    # 删除书籍
    path("deletebook/<int:id>/", views.deletbook, name="deletebook"),
    # 修改书籍
    path("updatabook/<int:id>/", views.updatebook, name="updatabook"),
    # 设置公告
    path("act/", views.announcement, name="act"),
    # 查看公告
    path("lookact/", views.lookannouncement, name="lookact"),
    # 添加学校
    path("shooladd/", views.shooladd, name="shooladd"),
    # 学校列表
    path("schoollist/", views.shoollist, name="shoollist"),
    #  删除学校
    path("deleteschool/<int:id>", views.deletschool, name="deletschool"),
    #  修改学校
    path("upschool/<int:id>", views.upschool, name="upschool"),
    #  学生添加
    path("addsut/", views.addstu, name="addsut"),
    # 学生列表
    path("stulist/", views.stulist, name="stulist"),
    # 删除学生
    path("deletstu/<int:id>/", views.deletsut, name="delets"),
    path("upsut/<int:id>/", views.upsut, name="upsut"),
    # 订单列表
    path("Orderslist/", views.order, name="Orderslist"),
    path("saut/", views.saudit, name="saut"),
    path("upsaut/", views.sauditsh, name="upsaut"),
    path("delesaut/", views.deletsaud, name="deletsaud"),
    #图书大图片:
    path("bookimgbig",views.bookbig,name="bookbig"),
    #
    path("comment/",views.comment,name="comment"),
    path("bookor/",views.bookor,name="bookor"),
    path("usercom/",views.useror,name="useror"),
    path("ckzl/",views.ckzl,name="xkzl"),
    path("bjdd",views.classgeade,name="bjdd")
]
