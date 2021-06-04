from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView
# Create your views here.
from  .models import Book
class book(View):
        def get(self,request):
            return  render(request,"edit_book.html")
        def post(self, request):
            try:
                books=request.POST.dict()
                books.pop("csrfmiddlewaretoken")
                Book.objects.create(**books)
                return redirect("APP1:listbook")
            except Exception :
                dicts="请重新添加书籍"
                return render(request, "edit_book.html",locals())

class listbook(ListView):
            template_name = "book_list.html"
            paginate_by = 4
            # paginate_orphans = 1
            context_object_name = "books"
            page_kwarg = "fall"
            model =  Book
class dlebook(View):
    def get(self,request,pull):
        books=Book.objects.get(pk=pull)
        books.delete()
        return  redirect("APP1:listbook")

class  upbook(View):
        def get(self,request,pall):
            if pall != None :
                try:
                    books=Book.objects.get(pk=pall)
                    return render(request,"add_book.html",locals())
                except Exception :
                    tite ="获取的书籍不存在"
                    return  render(request,"add_book.html",locals())
            else:
                 return  redirect("APP1:listbook")
        def post(self,request,pall):
                try:
                        books=request.POST.dict()
                        books.pop("csrfmiddlewaretoken")
                        lens=len(list(books.values()))
                        if lens==5:
                            Book.objects.filter(pk=books["id"]).update(bookname=books["bookname"],
                            bookauthor=books["bookauthor"], bookprice=books["bookprice"],bookpublic=books["bookpublic"])
                            return redirect("APP1:listbook")
                        else:
                            tite = "不能为空"
                            return redirect("APP1:upbook", locals())

                except Exception :
                        tite="填写有误请重新填写"
                        return  redirect("APP1:upbook",locals())


