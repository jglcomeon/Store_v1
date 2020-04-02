from django.shortcuts import render

# Create your views here.
from cart.models import CartInfo
from goods.models import GoodsInfo
from tools.login_check import check_login
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q

#添加商品个数购物车
@check_login
def add_goods(request, goods_id):
    user = request.user
    num1 = int(request.GET.get('num'))

    try:
        cart = CartInfo.objects.get(good_id=goods_id,user_id=user.id)
        sum2 = cart.num+num1
        cart.sum = sum2*cart.gprice
        cart.num = sum2
        cart.save()
    except:
        goods = GoodsInfo.objects.filter(id=goods_id)[0]
        CartInfo.objects.create(good_id=goods_id, user_id=user.id, num=1,gtitle=goods.gtitle,gpic=goods.gpic,gunit=goods.gunit,gprice=goods.gprice,sum=goods.gprice)
    result = {'code': 200}
    return JsonResponse(result)
#获取购物车商品数量
@check_login
def get_count(request):
    user = request.user
    counts = CartInfo.objects.filter(user_id=user.id).aggregate(myCount=Count('id'))
    result = {'code':200,'count1':counts['myCount']}
    return JsonResponse(result)
#获取我的购物车信息
@check_login
def my_cart(request):
    user = request.user
    user_id=user.id
    carts = CartInfo.objects.filter(user_id=user_id)
    return render(request,'cart.html',locals())
#增加购物车商品数量
def add_cart(request):
    cart_id = int(request.GET.get('cart_id'))
    user_id = int(request.GET.get('user_id'))
    good_id = int(request.GET.get('good_id'))

    try:
        cart = CartInfo.objects.get(id=cart_id)


        good = GoodsInfo.objects.get(id=good_id)

        if good.gkucun == cart.num:
            carts = CartInfo.objects.filter(user_id=user_id)
            return render(request, 'cart.html', locals())

        cart.num = cart.num + 1
        cart.sum = cart.num*cart.gprice
        cart.save()

    except:
        carts = CartInfo.objects.filter(user_id=user_id)
        return render(request, 'cart.html', locals())
    carts = CartInfo.objects.filter(user_id=user_id)
    return render(request, 'cart.html', locals())
#减少购物车商品数量
def dec_cart(request):
    cart_id = int(request.GET.get('cart_id'))
    user_id = int(request.GET.get('user_id'))
    good_id = int(request.GET.get('good_id'))
    try:
        cart = CartInfo.objects.get(id=cart_id)
        good = GoodsInfo.objects.get(id=good_id)
        if cart.num == 1:
            carts = CartInfo.objects.filter(user_id=user_id)
            return render(request, 'cart.html', locals())
        cart.num = cart.num - 1
        cart.sum = cart.num * cart.gprice
        cart.save()
    except:
        carts = CartInfo.objects.filter(user_id=user_id)
        return render(request, 'cart.html', locals())
    carts = CartInfo.objects.filter(user_id=user_id)
    return render(request, 'cart.html', locals())
#删除购物车某件商品
def delete_cart(request):
    id = request.GET.get('id')

    try:
        cart = CartInfo.objects.get(id=id)
        cart.delete()
    except:
        return HttpResponse('删除失败，请稍后重试')
    carts = CartInfo.objects.filter(user_id=cart.user_id)
    return render(request,'cart.html',locals())




