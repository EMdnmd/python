import json
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from CollegeInformationSubscription import settings
from CollegeInformationSubscription.settings import STATICFILES_DIRS
from systemadministrator import file_dispose
from systemadministrator.models import Register, Books, Notices, SchoolData, StudentData, Orders, Datas, Comments


# 后台首页
def index(request):
    return render(request, "systemadministrator/admin.html")


def home(request):
    register=Register.objects.count()
    school=SchoolData.objects.count()
    student=StudentData.objects.count()
    gly=StudentData.objects.filter(stuentjurisdiction=1).count()
    books=Books.objects.count()
    datas=Datas.objects.filter(datasaudit=0).count()
    return render(request, "systemadministrator/home.html",locals())


# 用户注册
def userRegistration(request):
    if request.method == "POST":
        users = request.POST.dict()
        error = ""
        user = users["user"]
        password = users["password"]
        passwords = users["passwords"]
        username = users["username"]
        if len(user) == 8:
            if len(password) >= 6:
                if passwords == password:
                    useridct = {'account': user, "name": username, "password": password}
                    print("进来了")
                    try:
                        Register.objects.create(**useridct)
                        return redirect("/login/")
                    except Exception as a:
                        print(a)
                        error = "账号已被注册"
                else:
                    error = "密码输入不正确"
            else:
                error = "密码不能低于6位"
        else:
            error = "请输入8位学号"
        return render(request, "systemadministrator/userRegistration.html", locals())
    return render(request, "systemadministrator/userRegistration.html")


def ztlogin(request):
    return redirect("/login/")


def administratorLogin(request):
    if request.method == "POST":
        users = request.POST.dict()
        user = users["user"]
        password = users["password"]
        useridct = {'account': user, "password": password}
        users = Register.objects.filter(**useridct)
        print("尽量ILE")
        if user == "admin" and password == "root":
            # 设置管理员权限
            request.session["jd"] = 2
            # 设置管理员身份
            request.session["iy"] = "管理员"
            # 设置管理员身份
            request.session["name"] = "root"
            # 设置登录时间.
            request.session["time"] = datetime.now().strftime("%Y-%m-%d %m:%d")
            # 设置管理员id
            request.session["id"] = 11111111
            request.session['bookidstr'] = []
            return redirect("Administrator:index")
        elif users:
            request.session["jd"] = 1
            # 设置学生身份
            request.session["iy"] = "学生"
            # 设置学生身份
            request.session["name"] = users.get().name
            # 设置登录时间.
            request.session["time"] = datetime.now().strftime("%Y-%m-%d %m:%d")
            # 设置学生id
            request.session["id"] = users.get().id
            request.session['bookidstr'] = []
            return redirect("/index/")
        else:
            erro = "账号或密码错误"
            return render(request, "systemadministrator/administratorLogin.html", locals())
    return render(request, "systemadministrator/administratorLogin.html")


# 学生账号列表
def studentslist(request, pall=1):
    register = Register.objects.all()
    piblics = register.values_list()
    paginator = Paginator(piblics, 5)
    num = paginator.num_pages
    try:
        page = paginator.page(pall)
    except:
        if pall == 1:
            page = paginator.page(pall)
        page = paginator.page(pall - 1)

    return render(request, "systemadministrator/Studentsmessage.html", locals())


# 删除学生账号
def delets(request, id):
    try:
        delet = Register.objects.get(pk=id)
        delet.delete()
        return HttpResponse("删除成功")
    except Exception as  e:
        return HttpResponse("删除失败")


# 添加学生
def addstudents(request):
    if request.method == "POST":
        users = request.POST.dict()
        error = ""
        user = users["user"]
        password = users["password"]
        passwords = users["passwords"]
        username = users["username"]
        if len(user) == 8:
            if len(password) >= 6:
                if passwords == password:
                    useridct = {'account': user, "name": username, "password": password}
                    try:
                        Register.objects.create(**useridct)
                        return redirect("Administrator:studentslist")
                    except Exception as a:
                        error = "账号已被注册"
                else:
                    error = "密码输入不正确"
            else:
                error = "密码不能低于6位"
        else:
            error = "请输入8位学号"
        return render(request, "systemadministrator/Studentaddhtml.html", locals())
    return render(request, "systemadministrator/Studentaddhtml.html")


# 修改学生密码
def updatastudents(request, id):
    updata = Register.objects.get(pk=id)
    if request.method == "POST":
        error = ""
        ids = request.POST.get("id")
        user = request.POST.get("user")
        username = request.POST.get("username")
        password = request.POST.get("password")
        passwords = request.POST.get("passwords")
        if len(user) == 8:
            if passwords == password:
                try:
                    Register.objects.filter(id=ids).update(
                        account=user, name=username, password=password)
                    return redirect("Administrator:studentslist")
                except:
                    error = "用户名已存在"
            else:
                error = "密码输入不正确"
        else:
            error = "请输入8位数id"
        return render(request, "systemadministrator/updatastudents.html", locals())
    return render(request, "systemadministrator/updatastudents.html", locals())


def addbook(request):
    fis = ""
    if request.method == "POST":
        er = ""
        try:
            booking = request.FILES.get("bookimgurl")
            file = file_dispose.fileUoload(booking, is_randomnane=True)
            filebook = settings.MEDIA_ROOT[0]
            fis = file.file_judge(filebook)[1]
        except:
            er = "你上传的图片有问题"
        dicts = request.POST.dict()
        dicts["bookimgurl"] = fis
        try:
            Books.objects.create(**dicts)
            return redirect("Administrator:booklist")
        except Exception as  e:
            print(e)
            er = "保存书籍有误"
        return render(request, "systemadministrator/addbook.html", locals())
    return render(request, "systemadministrator/addbook.html")


# 书籍列表
def booklist(request, pall=1):
    book = Books.objects.all()
    piblics = book.values_list()
    paginator = Paginator(piblics, 5)
    try:
        num = paginator.num_pages
        page = paginator.page(pall)
    except:
        if pall == 1:
            page = paginator.page(pall)
        page = paginator.page(pall - 1)
    return render(request, "systemadministrator/booklist.html", locals())


# 删除书籍
def deletbook(request, id):
    try:
        delet = Books.objects.get(pk=id)
        delet.delete()
        return HttpResponse("删除成功")
    except Exception as  e:
        return HttpResponse("不可以删除此书 有关联订单")


# 编辑图书
def updatebook(request, id):
    book = Books.objects.get(pk=id)
    if request.method == "POST":
        ids = request.POST.get("id")
        bookname = request.POST.get("bookname")
        bookprice = request.POST.get("bookprice")
        bookauthor = request.POST.get("bookauthor")
        bookimgurl = request.FILES.get("bookimgurl")
        bookbrief = request.POST.get("bookbrief")
        if bookimgurl == None:
            bookimgurl = book.bookimgurl
        else:
            file = file_dispose.fileUoload(bookimgurl, is_randomnane=True)
            filebook = settings.MEDIA_ROOT[0]
            bookimgurl = file.file_judge(filebook)[1]
        if bookbrief == "":
            bookbrief = book.bookbrief
        Books.objects.filter(id=ids).update(bookname=bookname, bookprice=bookprice, bookauthor=bookauthor,
                                            bookimgurl=bookimgurl, bookbrief=bookbrief)
        return redirect("Administrator:booklist")
    return render(request, "systemadministrator/updatabook.html", locals())


# 公告
def announcement(request):
    data = {"resq": ""}
    if request.method == "POST":
        no = Notices.objects
        try:
            act = request.POST.dict()
            if act != None:
                ms = no.all()
                if ms:
                    ms[0].delete()
            no.create(**act)
            data["resq"] = "设置成功"
        except Exception as  e:
            print(e)
            data["resq"] = "设置失败"
        return HttpResponse(json.dumps(data))
    return render(request, "systemadministrator/setTheAnnouncement.html")


# 查看公告
def lookannouncement(request):
    no = Notices.objects.all()
    return HttpResponse(no[0].noticestring)


# 学校添加
def shooladd(request):
    if request.method == "POST":
        datas = {"resq": ""}
        shool = request.POST.dict()
        s = shool["year"].split("-")[0]
        shool["grade"] = s + "级"
        try:
            SchoolData.objects.create(**shool)
            datas["resq"] = "保存成功"
        except Exception as  E:
            print(E)
            datas["resq"] = "保存失败"
        return HttpResponse(json.dumps(datas))
    return render(request, "systemadministrator/shooladd.html")


def shoollist(request):
    school = SchoolData.objects.all()
    schoollist = school.values_list()
    s = request.GET.get("id", 1)
    pag = Paginator(schoollist, 5, 1)
    try:
        page = pag.page(s)
    except:
        if s == 1:
            page = pag.page(s)
        page = pag.page(s - 1)
    return render(request, "systemadministrator/shoollist.html", locals())


def deletschool(request, id):
    try:
        delet = SchoolData.objects.get(pk=id)
        delet.delete()
        return HttpResponse("删除成功")
    except Exception as  e:
        print(e)
        return HttpResponse("抱歉请先删除此专业的学生")


def upschool(request, id):
    so = SchoolData.objects
    if request.method == "POST":
        schools = request.POST.dict()
        try:
            so.filter(id=schools["id"]).update(college=schools["college"], specialty=schools["specialty"])
            return redirect("Administrator:shoollist")
        except Exception  as e:
            s = "保存失败"
    SchoolDatas = so.get(pk=id)
    return render(request, "systemadministrator/upschool.html", locals())


# 添加学生
def addstu(request):
    so = SchoolData.objects
    if request.method == "POST":
        sut = request.POST.dict()
        if sut["studentnumber"].isdigit():
            sut["studentschool"] = so.get(pk=sut["studentschool"])
            StudentData.objects.create(**sut)
            return redirect("Administrator:stulist")
        else:
            ls = "学号必须位8位数字"
            school = so.all()
            return render(request, "systemadministrator/addsut.html", locals())
    school = so.all()
    return render(request, "systemadministrator/addsut.html", locals())


# 学生列表
def stulist(request):
    stu = StudentData.objects.all()
    id = request.GET.get("id", 1)
    page = Paginator(stu, 5, 1)
    try:
        pages = page.get_page(id)
    except:
        if id == 1:
            pages = page.get_page(id)
        pages = page.get_page(id - 1)

    return render(request, "systemadministrator/sutlist.html", locals())


# 编辑学生
def deletsut(request, id):
    print("进来了")
    try:
        delet = StudentData.objects.get(pk=id)
        delet.delete()
        return HttpResponse("删除成功")
    except Exception as  e:
        return HttpResponse("删除失败")


def upsut(request, id):
    ms = ""
    try:
        up = StudentData.objects.get(pk=id)
        if up.stuentjurisdiction == 0:
            up.stuentjurisdiction = 1
            up.save()
            ms = "管理员设置成功"
        else:
            up.stuentjurisdiction = 0
            up.save()
            ms = "已撤销此学生管理员权限"
        return HttpResponse(ms)
    except Exception as  e:
        return HttpResponse("删除失败")


def order(request):
    orders = Orders.objects.all()
    return render(request, "systemadministrator/orders.html", locals())


def tuichudengl(request):
    del request.session["id"]
    return redirect("/login/")


def page_not_found(request, exception):
    # 全局404处理函数
    return HttpResponse("页面未找到")


def page_error(request):
    # 全局处理500
    return HttpResponse("服务器错误")


def saudit(request):
    id=request.GET.get("id",1)
    ads = Datas.objects.all()
    ada=Paginator(ads,5,1)
    try:
        ad=ada.get_page(id)
    except:
        if id==1:
            ad = ada.get_page(id)
        else:
            ad = ada.get_page(id-1)

    return render(request, "systemadministrator/saudit.html", locals())


def sauditsh(request):
    ids = request.GET.get("id")
    sk = Datas.objects.get(pk=ids)
    print(sk.datasaudit)
    if sk.datasaudit == 0:
        sk.datasaudit = 1
        sk.save()
        ms = "审核通过"
    else:
        sk.datasaudit = 0
        sk.save()
        ms = "已撤销此资料"
    return HttpResponse(ms)


def deletsaud(request):
    id=request.GET.get("id")
    try:
        delet = Datas.objects.get(pk=id)
        delet.delete()
        return HttpResponse("删除成功")
    except Exception as  e:
        return HttpResponse("删除失败")


# 图书大图片
def bookbig(request):
    s1=request.GET.get("id")
    if request.method=="POST":
            ids=request.GET.get("id")
            bookimgurl=request.FILES.get("file")
            try:
                file = file_dispose.fileUoload(bookimgurl, is_randomnane=True)
                filebook = settings.MEDIA_ROOT[1]
                bookimgurl = file.file_judge(filebook)[1]
                book=Books.objects.get(pk=ids)
                book.bookimgbig=bookimgurl
                book.save()
                ditas={"code":0}
            except:
                ditas={"code":1}
            return  HttpResponse(json.dumps(ditas))
    return render(request,"systemadministrator/cogdigimg.html",locals())

# 通过学生查看订单
def comment(request):
        ps=request.GET.get("id")
        name=request.GET.get("name")
        sa=Orders.objects.filter(orderstudent=ps)
        return  render(request,"systemadministrator/comment.html",locals())

# 通过购买用户查看订单
def useror(request):
        id=request.GET.get("id")
        name=request.GET.get("name")
        sa = Orders.objects.filter(orderregister=id)
        return  render(request,"systemadministrator/useror.html",locals())



# 通过图书查看订单
def bookor(request):
    id = request.GET.get("id")
    name = request.GET.get("name")
    sa = Orders.objects.filter(orderbook=id)
    return render(request, "systemadministrator/booker.html", locals())

def classgeade(request):
        cl=request.GET.get("class")
        cla=StudentData.objects.filter(classgrade=cl)
        la=[]
        for i in cla:
                for s  in i.student.all():
                    la.append(s)
        return  render(request,"systemadministrator/upsut.html",locals())


def ckzl(request):
         id=request.GET.get("id")
         data=Datas.objects.get(pk=id)

         return render( request,"systemadministrator/imgck.html",locals())








