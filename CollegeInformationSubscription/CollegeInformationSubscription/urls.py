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
from django.urls import path, include

from systemadministrator import views
from buysystem import views as bv

urlpatterns = [
    path("",views.ztlogin),
    path('index/', bv.index),
    path("login/", views.administratorLogin,),
    # 注册页面
    path("userregister/", views.userRegistration,),
    path("APP1/", include("systemadministrator.urls")),
    path("APP2/", include("buysystem.urls")),
    path("tc/", views.tuichudengl, name="tc"),

]
handler404 = views.page_not_found
handler500 = views.page_error
