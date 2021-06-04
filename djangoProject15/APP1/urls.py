"""djangoProject15 URL Configuration

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
from  . import views
from  .  import viewstwo,vivethree
app_name="APP1"
urlpatterns = [
        path("addbook/",views.book.as_view(),name="addbook"),
        path("listbook/", views.listbook.as_view(), name="listbook"),
        path("listbook/<int:fall>", views.listbook.as_view(), name="listbook"),
        path("dlebook/<int:pull>", views.dlebook.as_view(), name="dle"),
        path("upbook/<int:pall>",views.upbook.as_view(),name="upbook"),
        path("buybook/", viewstwo.buy_books.as_view(), name="butybook"),
        path("buybooklist/", viewstwo.listbuybook.as_view(), name="butybooklist"),
        path("buybooklist/<int:fall>", viewstwo.listbuybook.as_view(), name="butybooklist"),
        path("sheet/", viewstwo.listsheet.as_view(), name="listsheet"),
        path("sheet/<str:pall>", viewstwo.listsheet.as_view(), name="listsheet"),
        path("sheet/<str:pall>/<int:fall>",viewstwo.listsheet.as_view(),name="listsheet"),
        path("registre/",vivethree.register.as_view(),name="registre"),
        path("login/", vivethree.login.as_view(), name="login"),
        path("logout/",vivethree.exits.as_view(),name="exit")

]
