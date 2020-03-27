import jwt
from django.http import JsonResponse
from user.models import  User
KEY_A = 'jjg'
def check_login(func):
    def wrapper(request,*args,**kwargs):
        #获取token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            token = request.GET.get('token')
            if not token:
                token = request.POST.get('token')

        if not token:
            result = {'code':109,'error':'need token'}
            return JsonResponse(result)
        try:
            res = jwt.decode(token,KEY_A,algorithm='HS256')
        except Exception as e:
            print('login check is error%s'%(e))
            result = {'code':108,'error':'the token is wrong'}
            return JsonResponse(result)
        #token校验成功

        username = res['username']

        try:
            user=User.objects.get(name=username)
        except:
            user=None
        if not user:
            result = {'code':110,'error':'the user is not existed'}
            return JsonResponse(result)
        #将user赋值给request对象
        request.user = user
        return func(request,*args,**kwargs)
    return wrapper