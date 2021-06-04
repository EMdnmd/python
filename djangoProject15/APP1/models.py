from datetime import datetime

from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    bookname = models.CharField(max_length=20,unique=True)
    bookauthor=models.CharField(max_length=10,default="空")
    bookprice = models.FloatField(default=20.00)
    bookpublic = models.CharField(max_length=20)
    bookaddtime = models.DateTimeField(auto_now_add=datetime.now)

    class Meta:
        db_table = "Book"




class user(models.Model):
    di = models.AutoField(primary_key=True)
    username=models.CharField(max_length=20,unique=True)
    password=models.CharField(max_length=100)
    phone=models.CharField(unique=True,max_length=11)
    email=models.CharField( max_length=20,unique=True,null=True)
    age=models.IntegerField(null=True)
    sex =models.CharField( max_length=2,null=True)
    time=models.DateTimeField(auto_now_add=datetime.now)
    login_type = ((1, '允许登录'), (2, '禁⽌登录'))  # ⽤户⾃定义类型对应
    allowed = models.IntegerField(default=1, choices=login_type)
    name=models.CharField(max_length=20,default="空")
    class Meta:
        db_table="user"

class Bookfigure(models.Model):
    di = models.AutoField(primary_key=True)
    user=models.ForeignKey(user,models.CASCADE, related_name="user" , null=False,default=0)
    book = models.ForeignKey(Book, models.CASCADE, related_name="book",null=False,default=0)
    class Meta:
        db_table = "Bookfigure"
