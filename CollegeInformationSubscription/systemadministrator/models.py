from datetime import datetime

from django.db import models

# Create your models here.


# 注册表
class Register(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=16,unique=True)  # 账号
    name = models.CharField(max_length=16)  # 姓名
    password = models.CharField(max_length=32)  # 密码
    class Meta:
            db_table="Register"

# 学校信息表
class SchoolData(models.Model):

    id = models.AutoField(primary_key=True)
    college = models.CharField(max_length=16)  # 学院
    specialty = models.CharField(max_length=32)  # 专业
    year = models.DateTimeField()  # 入学年份
    grade=models.CharField(max_length=10,default="空")

    class Meta:
            db_table="SchoolData"

# 学生信息表
class StudentData(models.Model):
    id = models.AutoField(primary_key=True)
    studentnumber = models.IntegerField(unique=True)  # 学号 唯一
    studentgender = models.CharField(max_length=2)  # 性别
    studentname = models.CharField(max_length=16)  # 姓名
    stuentjurisdiction = models.IntegerField(default=0)  # 权限 0表示普通学生 1表示班级负责人
    studentschool = models.ForeignKey(to='SchoolData', on_delete=models.DO_NOTHING)  # 学校信息表id
    classgrade = models.CharField(max_length=16,default="空")  # 班级
    class Meta:
            db_table="StudentData"

# 图书表
class Books(models.Model):
    id = models.AutoField(primary_key=True)
    bookname = models.CharField(max_length=32)  # 图书名
    bookimgurl = models.CharField(max_length=150)  # 图书图片url
    bookprice = models.IntegerField()  # 图书价格
    bookbrief=models.TextField(default="空")#图书简介
    bookauthor=models.CharField(max_length=20,default="空")#图书作者
    bookimgbig=models.CharField(max_length=40,default="空")#图书大图片
    class Meta:
        db_table = "Books"


# 订单表
class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    ordernumber = models.CharField(max_length=32)  # 订单号  唯一 日期+随机数
    ordertime = models.DateTimeField()  # 订单时间
    orderprice = models.IntegerField()  # 总价
    orderregister = models.ForeignKey(to='Register', on_delete=models.DO_NOTHING)  # 注册表id
    orderbook = models.ForeignKey(to='Books', on_delete=models.DO_NOTHING)  # 图书表id
    orderstudent = models.ForeignKey(to='StudentData', on_delete=models.DO_NOTHING,related_name="student")  # 学生信息表id
    class Meta:
        db_table = "Orders"

# 资料表
class Datas(models.Model):
    id = models.AutoField(primary_key=True)
    dataname = models.CharField(max_length=32)  # 资料名
    dataimgurl = models.CharField(max_length=64)  # 资料图片url
    dataintroduce = models.CharField(max_length=128)  # 资料简介
    qqnumber = models.IntegerField(default=0)  # QQ号
    dataauthor = models.CharField(max_length=20, default="空")  # 资料作者
    dataregister = models.ForeignKey(to='Register', on_delete=models.DO_NOTHING)  # 注册表id
    datasaudit=models.IntegerField(default=0)
    class Meta:
        db_table = "Datas"

# 评论表
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    commentstring = models.CharField(max_length=50)  # 评论内容
    commenttime = models.DateTimeField(auto_now_add=datetime.now)
    commentstudent = models.ForeignKey(to='Books', on_delete=models.DO_NOTHING,related_name="books")  # 图书表id
    commentregister = models.ForeignKey(to='Register', on_delete=models.DO_NOTHING)  # 注册表id
    class Meta:
        db_table = "Comments"

# 公告表
class Notices(models.Model):
    id = models.AutoField(primary_key=True)
    noticestring = models.CharField(max_length=50)  # 公告内容
    noticetime = models.DateTimeField(auto_now_add=datetime.now)  # 公告时间
    noticestate = models.IntegerField(default=1)  # 公告状态  0表示历史  1表示最新
    class Meta:
        db_table = "Notices"