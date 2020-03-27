from django.conf.urls import url
from .  import views
urlpatterns=[
    url(r'^/add_goods/(\d+)$',views.add_goods),
    url(r'^/get_count$',views.get_count),
    url(r'^/my_cart$',views.my_cart),
    url(r'^/add_cart$',views.add_cart),
    url(r'^/dec_cart$',views.dec_cart),
    url(r'/delete$',views.delete_cart),
    ]