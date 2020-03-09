import hashlib
import time

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.template import loader
from goods.models import TypeInfo

from tools.login_check import check_login

# Create your views here.
from user.models import User
import jwt
KEY_A = 'jjg'

#使用jwt生成token
def make_token(username):
    times =time.time()
    username = jwt.encode({'username':username,'exp':times+300,},key=KEY_A,algorithm='HS256')
    return username


#注册
def register_view(request):
    if request.method=='GET':
        return render(request,'register.html')
    elif request.method=='POST':
        name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        s = hashlib.sha256()
        s.update(pwd.encode())
        pwd1 = s.hexdigest()

        email = request.POST.get('email')
        try:
            User.objects.create(name=name,pwd=pwd1,email=email)
            html='<a href="/user/login">请登陆</a>'
            return HttpResponse('注册成功'+html)
        except:
            return HttpResponse('注册失败,请稍后重试')
#检查邮箱是否注册
def check_eamil(request):
    email = request.GET.get('email')
    try:
        email=User.objects.get(email=email)
        return HttpResponse("0")
    except:
        return HttpResponse("1")
#检查用户名是否注册
def check_name(request):
    name = request.GET.get('name')
    try:
        name = User.objects.get(name=name)
        return HttpResponse("0")
    except:
        return HttpResponse("1")
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        #print(pwd)
        p_m=hashlib.sha256()
        p_m.update(pwd.encode())
        p_m=p_m.hexdigest()
        print(p_m)
        checkd = request.POST.get('r_m')
        try:
            User.objects.get(name=name,pwd=p_m)
            if checkd:
                request.session['username']= name
            token = make_token(name).decode()
        except:
            result = {'code':101,'err_info':"用户名账号或密码错误"}
            return JsonResponse(result)
        result = {'code':200,'username':name,'token':token}
        return JsonResponse(result)
def index(request):
    name = request.GET.get('name')
    types = TypeInfo.objects.all()
    new_fruits = types[0].goodsinfo_set.filter()[0:4]
    sea_foods = types[1].goodsinfo_set.filter()[0:4]
    poultry_foods = types[2].goodsinfo_set.filter()[0:4]
    eggs = types[3].goodsinfo_set.filter()[0:4]
    organic_vegetable = types[4].goodsinfo_set.filter()[0:4]
    drinks = types[5].goodsinfo_set.filter()[0:4]


    return render(request,'index.html',locals())

@check_login
def user_center(request):
    if request.method == 'POST':
        user = request.user
        result = {'code':200,'username':user.name}
        return JsonResponse(result)
    elif request.method == 'GET':
        token = request.GET.get('token')
        res = jwt.decode(token, KEY_A, algorithm='HS256')
        try:
            user = User.objects.get(name=res['username'])
        except:
            return HttpResponse('非法访问！')

        return render(request,'user_center_info.html',locals())




