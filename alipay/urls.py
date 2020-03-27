from django.conf.urls import url
from . import views
urlpatterns = [
    url('create_order$',views.create_order),
    url('create_order1$',views.create_order1),
    url('index/',views.index),#处理订单
    url('pay_result',views.pay_result),#支付宝处理完成后回调的get请求路由
    url('update_order',views.update_order),#支付宝处理完成后回调的post请求路由
    url('my_order',views.my_order),
]