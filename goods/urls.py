from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'/detail$',views.goods_detail),
    url(r'/recommend1',views.get_recommend1),
    #根据人气给出商品列表
    url(r'/list$',views.good_list),
    #根据价格获取商品列表
    url(r'/list1$',views.good_list1),
    url(r'/search$',views.good_serch),

]