import time
from urllib.parse import parse_qs
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from alipay.models import Order, Order_detail
from cart.models import CartInfo
from goods.models import GoodsInfo

from tools.alipay import AliPay
import json

from tools.login_check import check_login
from user.models import Address
from django.core import serializers


def aliPay():
    obj = AliPay(
    appid="2021001145618200",               # 支付宝沙箱里面的APPID，需要改成你自己的
    app_notify_url="http://127.0.0.1:8000/pay/update_order", # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
    return_url="http://127.0.0.1:8000/pay/pay_result",      # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
    alipay_public_key_path=settings.ALIPAY_PUBLIC, # 支付宝公钥
    app_private_key_path=settings.APP_PRIVATE,   # 应用私钥
    debug=False, # 默认False,True表示使用沙箱环境测试
  )

  # 优化:在settings里面的设置后使用
  # obj = AliPay(
  #   appid=settings.APPID,
  #   app_notify_url=settings.NOTIFY_URL,
  #   return_url=settings.RETURN_URL,
  #   alipay_public_key_path=settings.PUB_KEY_PATH,
  #   app_private_key_path=settings.PRI_KEY_PATH,
  #   debug=True,
  # )
    return obj
#立即购买
@check_login
def create_order1(request):
    user = request.user
    good_id = request.POST.get('good_id')
    num = request.POST.get('num')
    sum = request.POST.get('sum')
    print(good_id,sum,num,user.id)
    order_no =int(str(user.id)+str(int(time.time())))
    try:
        Order.objects.create(order_no=order_no, money=sum, user_id_id=user.id)
        good = GoodsInfo.objects.get(id=good_id)
        Order_detail.objects.create(good_id=good_id, num=num,
                                    order_id_id=order_no, sum=sum, gtitle=good.gtitle, gpic=good.gpic,
                                    gprice=good.gprice, gunit=good.gunit)
    except Exception as e:
        print(e)
        result = {'code': 502, 'error': '创建订单失败请稍后重试'}
        return JsonResponse(result)
    result = {'code': 200, 'order_no': order_no}
    return JsonResponse(result)

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        order = json.loads(request.POST.get('order'))
        user_id = order.get('user_id')
        order_no = int(str(user_id)+str(int(time.time())))
        money = order.get('sum')
        data = json.loads(request.POST.get('data'))

        try:
            Order.objects.create(order_no=order_no, money=money,user_id_id=user_id)
        except Exception as e:
            print(e)
            result = {'code': 502, 'error': '创建订单失败请稍后重试'}
            return JsonResponse(result)

        for info in data:
            try:
                #print(info.get('good_id'),info.get('user_id'))
                good = GoodsInfo.objects.get(id=info.get('good_id'))
                Order_detail.objects.create(good_id=info.get('good_id'), num=info.get('num'),
                                            order_id_id=order_no, sum=info.get('sum'),gtitle=good.gtitle,gpic=good.gpic,gprice=good.gprice,gunit=good.gunit)

                cart = CartInfo.objects.get(good_id=info.get('good_id'), user_id=info.get('user_id'))
                cart.delete()

            except Exception as e:
                print(e)
                result = {'code': 502, 'error': '创建订单失败请稍后重试!'}
                return JsonResponse(result)

        result = {'code':200,'order_no':order_no}
        return JsonResponse(result)
    if request.method == 'GET':
        order_id = request.GET.get('order_no')
        try:
            order = Order.objects.get(order_no=order_id)
            #获取订单商品详情
            order_detail = Order_detail.objects.filter(order_id_id=order_id)
            count = order_detail.count()
            user_id = order.user_id_id
            try:
                address = Address.objects.get(user_id_id=user_id)
            except:
                return HttpResponse("请到个人中心填写地址！")
        except:
            return HttpResponse("请稍后重试！")



        return render(request,'order.html',locals())
@check_login
def my_order(request):
    if request.method == 'POST':
        user = request.user
        orders = Order.objects.filter(user_id_id=user.id)
        data={}
        orders1=[serializers.serialize('json',orders)]

        for order in orders:
            list=[]
            order_detail = Order_detail.objects.filter(order_id_id=order.order_no)
            #for i in order_detail:
            list.append(serializers.serialize("json",order_detail))
            data[order.order_no]=list


        print('data len is %d，orders len is %d'%(len(data),len(orders1)))
        result = {'data':data,'orders':orders1}



        return JsonResponse(result)





@csrf_exempt
def index(request):
     # 实例化SDK里面的类AliPay
    alipay = aliPay()
    order_no = request.GET.get('order_no')
    money = request.GET.get('money')






    # 对购买的数据进行加密
    # 保留俩位小数 前端传回的数据

    # 商户订单号  # 订单号可以有多中生成方式，可以百度一下
    # 1. 在数据库创建一条数据：状态（待支付）




    query_params = alipay.direct_pay(
    subject="123", # 商品简单描述 这里一般是从前端传过来的数据
    out_trade_no=order_no, # 商户订单号 这里一般是从前端传过来的数据
    total_amount=float(money), # 交易金额(单位: 元 保留俩位小数)  这里一般是从前端传过来的数据
  )
    # 拼接url，转到支付宝支付页面
    pay_url = "https://openapi.alipay.com/gateway.do?{}".format(query_params)
    #result = {'code':200,'url':pay_url}
    #print(pay_url)

    return redirect(pay_url)
@csrf_exempt
def update_order(request):
    """支付成功后，支付宝向该地址发送post请求"""
    if request.method == 'POST':
        print("haha")
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        alipay = aliPay()
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
        # 1.修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            #print(out_trade_no)
            try:
                order = Order.objects.get(order_no=out_trade_no)
                order.is_pay=1
                order.save()
            except:
                return HttpResponse('支付失败')

        # 2. 根据订单号将数据库中的数据进行更新
            return HttpResponse('支付成功')

        else:
            return HttpResponse('支付失败')

    return HttpResponse('')
@csrf_exempt
def pay_result(request):
    #支付完成后，跳转回的地址
    params = request.GET.dict()
    out_trade_no = request.GET.get('out_trade_no')
    sign = params.pop('sign', None)
    alipay = aliPay()
    status = alipay.verify(params, sign)
    html="""<a href="/user/index">返回<a>"""
    if status:
        try:
            order = Order.objects.get(order_no=out_trade_no)
            order.is_pay = 1
            order.save()
        except:
            return HttpResponse('支付失败')
        return HttpResponse('支付成功，点击 '+html)

    return HttpResponse('支付失败,点击 '+html)
