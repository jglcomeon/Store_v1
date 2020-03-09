from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'/register',views.register_view),
    url(r'/check_email$',views.check_eamil),
    url(r'/check_name$',views.check_name),
    url(r'/login$',views.login),
    url(r'/index$',views.index),
    url(r'/user_center$',views.user_center),
]