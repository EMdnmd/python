from django.shortcuts import redirect, render, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from systemadministrator import urls as  surls
from buysystem import urls  as bsurls


class migglew(MiddlewareMixin):
    def process_request(self, request):
        rounte = ["/userregister/", "/login/"]
        user = request.session.get("id")
        if user:
            return None
        elif request.path in rounte:
            return None
        elif request.path not in 'login':
            return redirect("/login/")
    # 权限
    def process_view(self, request, view_func, view_args, view_kwargs):
        if  request.session.get("id") :
            if jd(request):
                return None
            else:
                return  render(request,"systemadministrator/403.HTML")
        else:
             return None
    def process_template_response(self, request, response):
         return None
    def process_response(self, request, response):
        if 400 <= response.status_code < 500:
            return render(request, "systemadministrator/404.html")
        elif response.status_code == 500:
            return render(request, "systemadministrator/500.html")
        return response

def jd(request):
    jd = request.session["jd"]
    try:
        if jd==2:
                return  True
        elif jd==1:
                path=["APP1"]
                paths=request.path.split("/")
                if paths[1] in path:
                        return False
                else:
                    return  True
    except:
            return  True

