import json
import random
import time

from CollegeInformationSubscription import settings
from CollegeInformationSubscription.settings import STATICFILES_DIRS
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from systemadministrator import models as systemadminmodels, file_dispose



# Create your views here.

def ls():
    sc = systemadminmodels.SchoolData.objects
    k1 = sc.all()
    ls = []
    for i in k1:
        for j in ls:
            if i.college == j["name"]:
                break
        else:
            ls.append({"name": i.college, 'cityList': []})
    for m in ls:
        k = sc.filter(college=m["name"])
        for i in k:
            for s in m["cityList"]:
                if i.specialty in s["name"]:
                    break
            else:
                m["cityList"].append({"name": i.specialty, "areaList": []})
    for i in ls:
        for m in i["cityList"]:
            k = sc.filter(college=i["name"], specialty=m["name"])
            for s in k:
                for l in m["areaList"]:
                    if s.grade in l:
                        break
                else:
                    m["areaList"].append(s.grade)

    # print(ls)
    return ls


def book_json(sql_list):
    book_dict_json = {}
    book_list = []
    count = 1
    for book_item in sql_list:
        book_dict = {}
        # print(book_item.id)
        book_dict["id"] = book_item.id
        book_dict["bookimg"] = book_item.bookimgurl
        book_dict["bookname"] = book_item.bookname
        book_dict["bookauthor"] = book_item.bookauthor
        book_dict["bookintroduction"] = book_item.bookbrief
        book_dict["bookprice"] = book_item.bookprice
        book_dict["right"] = book_item.id
        book_list.append(book_dict)
        count += 1
    book_dict_json["name"] = book_list
    return book_dict_json


# 主页
def index(request):
    if request.method == "POST":
        book_dict_json = book_json(systemadminmodels.Books.objects.all())
        return JsonResponse(book_dict_json)
    try:
        noticetime = systemadminmodels.Notices.objects.first().noticetime
        noticestring = systemadminmodels.Notices.objects.first().noticestring
    except:
        return render(request, "frontsytem/index.html", locals())
    return render(request, "frontsytem/index.html", locals())


def comment_ajax_json(sql_list):
    print(sql_list)
    data = {}
    bookname = []
    for book_comment in sql_list:
        buffer = {
            'name': book_comment.commentregister.name,
            "comment": book_comment.commentregister.account,
            "time": str(book_comment.commenttime)
        }
        bookname.append(buffer)
        data["book_comment"] = bookname
    # ls = json.dumps({'msg': data}, ensure_ascii=False)
    ls = data
    return ls


# 图书详情页
# 图书详情页
def details(request):
    if request.GET.get("pl") == '1':
        book_id = request.GET.get('book_id')
        comment = systemadminmodels.Comments.objects.filter(commentstudent_id=book_id).all()
        print(comment)
        ls = comment_ajax_json(comment)
        return JsonResponse(ls)

    book_id = request.GET.get("id")
    print(book_id)
    book_list = systemadminmodels.Books.objects.get(id=book_id)
    return render(request, "frontsytem/details.html", locals())

# 图书添加评论
def addcomment(request):
    err = ''
    if request.method == "POST":

        commentregister = request.POST.get("register_id")
        commentbook = request.POST.get("book_id")
        commentstring = request.POST.get("comment")
        if commentregister:
            systemadminmodels.Comments.objects.create(commentstring=commentstring, commentregister_id=commentregister, commentstudent_id=commentbook)
            return redirect("/APP2/index/")
        else:
            return redirect("/APP1/login/")
    else:
        book_id = request.GET.get("id")
        regster_id = request.session.get("id")
        return render(request, "frontsytem/addcomment.html", locals())


# 生成随机数
def get_random_num():
    num = random.randint(1000, 9999)
    return num


def sub_if(request, studentnumber, classgrade, studentgender, studentname, shcool_id):
    try:
        if len(studentnumber) == 8:
            if systemadminmodels.StudentData.objects.filter(studentnumber=int(studentnumber)).all():
                print()
            else:
                systemadminmodels.StudentData.objects.create(classgrade=classgrade, studentgender=studentgender,
                                                             studentnumber=int(studentnumber), studentname=studentname,
                                                             studentschool_id=shcool_id)
        else:
            err = "请输入八位学号"
            return render(request, 'frontsytem/submitorder.html', {"err": err})
    except Exception as e:
        return redirect("/APP2/order/")



@csrf_exempt
def submitorder(request):
    err = ""
    if request.method == "GET":
        if request.GET.get("json") == '1':
            sm = ls()
            return JsonResponse({"name": sm}, safe=False)
        return render(request, 'frontsytem/submitorder.html')
    if request.method == "POST":
        try:

            # 保存学生信息
            college = request.POST.get("college")
            specialty = request.POST.get("specialty")
            grade = request.POST.get("grade")
            shcool_id = systemadminmodels.SchoolData.objects.filter(college=college, specialty=specialty, grade=grade).first().id
            classgrade = request.POST.get("classgrade")
            studentnumber = request.POST.get("studentnumber")
            studentgender = request.POST.get("studentgender")
            studentname = request.POST.get("studentname")

            sub_if(request, studentnumber, classgrade, studentgender, studentname, shcool_id)

            # 保存订单
            now_time = time.strftime('%Y-%m-%d %H:%M:%S')
            register_id = request.session.get("id")
            student_id = systemadminmodels.StudentData.objects.filter(studentnumber=int(studentnumber), studentname=studentname, studentgender=studentgender, classgrade=classgrade).all()[0].id
            order_num = time.strftime('%Y%m%d') + str(get_random_num())
            order_time = now_time

            # book的id
            bookidlist = request.session['bookidstr'].split(",")
            print(bookidlist)
            zbookprice = 0
            for p in bookidlist:
                print(p)
                pricebuffer = int(systemadminmodels.Books.objects.filter(id=p).first().bookprice)
                zbookprice = zbookprice + pricebuffer
            print(zbookprice)

            for i in bookidlist:
                print(i)
                systemadminmodels.Orders.objects.create(ordernumber=order_num, ordertime=order_time,
                                                        orderprice=zbookprice, orderbook_id=i,
                                                        orderregister_id=register_id, orderstudent_id=student_id)

            return redirect("/APP2/order/")
        except Exception as e:
            err = "信息有误，请重试！"
            return render(request, 'frontsytem/submitorder.html', {"err": err})


def uploaddata(request):
    fis = ""
    bookqq = 0
    if request.method == "POST":
        err = ""
        try:
            dataimgurl = request.FILES.get("dataimgurl")
            file = file_dispose.fileUoload(dataimgurl, is_randomnane=True)
            filebook = settings.MEDIA_ROOT[0]
            fis = file.file_judge(filebook)[1]
        except:
            err = "你上传的图片有问题"
        dicts = request.POST.dict()

        dicts["dataimgurl"] = fis
        dicts["dataregister_id"] = request.session.get("id")
        print(dicts)
        try:
            systemadminmodels.Datas.objects.create(**dicts)
            return redirect("/index")
        except Exception as e:
            print(e)
            err = "保存书籍有误"
        return render(request, "frontsytem/uploaddata.html",locals())
    return render(request, "frontsytem/uploaddata.html")


def changepassword(request):
    err = ''
    if request.method == "POST":
        web_page_dict = request.POST.dict()
        print(web_page_dict)
        register_value = systemadminmodels.Register.objects.filter(account=web_page_dict["account"], name=web_page_dict["name"], password=web_page_dict["password"]).all()
        if register_value:
            if web_page_dict['newpassword1'] == web_page_dict['newpassword2']:
                if len(web_page_dict['newpassword2']) >= 6:
                    new_password = {'account': web_page_dict["account"], "name": web_page_dict["name"], "password": web_page_dict["newpassword2"]}
                    systemadminmodels.Register.objects.filter(account=web_page_dict["account"], name=web_page_dict["name"], password=web_page_dict["password"]).update(**new_password)
                    return  redirect("/tc/")
                else:
                    err = "新密码大于6位！"
            else:
                err = "两次新密码不一致！"
        else:
            err = "用户信息输入错误!"

    print(err)

    return render(request, "frontsytem/changepassword.html",locals())


def order(request):

    if request.GET.get("but") == '0':
        order_list = systemadminmodels.Orders.objects.filter(orderregister_id=request.session.get("id")).all()
        return render(request, "frontsytem/order.html", locals())
    elif request.GET.get("but") == '1':
        order_l = systemadminmodels.Orders.objects.filter(orderregister_id=request.session.get("id")).all()
        classgrade = order_l.first().orderstudent.classgrade

        order_class = systemadminmodels.StudentData.objects.filter(classgrade=classgrade).all()
        order_list = systemadminmodels.Orders.objects.filter(orderstudent__classgrade=classgrade).all()


        if order_l.first().orderstudent.stuentjurisdiction == 1:
            order_class = systemadminmodels.StudentData.objects.filter(classgrade=classgrade).all()
            order_list = systemadminmodels.Orders.objects.filter(orderstudent__classgrade=classgrade).all()
            print(order_list)
            return render(request, "frontsytem/order.html", locals())
        else:
            err = "权限不够，请联系管理员, 申请权限。"
            return render(request, "frontsytem/order.html", {"err":err})
    order_list = systemadminmodels.Orders.objects.filter(orderregister_id=request.session.get("id")).all()
    print(order_list)

    return render(request, "frontsytem/order.html", locals())


# book_id
def savebookid(request):
    del request.session['bookidstr']
    request.session['bookidstr'] = request.POST.get('bookid_str')
    return JsonResponse({"name": "ok!"})