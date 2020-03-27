from django.db import models

# Create your models here.
from user.models import User


class Order(models.Model):
    order_no = models.BigIntegerField(primary_key=True)
    is_pay = models.BooleanField(default=False)
    money = models.DecimalField(max_digits=7,decimal_places=2)
    user_id = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True,null=True)


    class Meta:
        db_table='order'

class Order_detail(models.Model):
    good_id = models.IntegerField()

    order_id = models.ForeignKey(Order)
    num = models.IntegerField()
    sum = models.DecimalField(max_digits=7,decimal_places=2)
    # 新增字段
    gtitle = models.CharField(max_length=20,null=True)
    gpic = models.ImageField(upload_to='goods',null=True)
    gprice = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    gunit = models.CharField(max_length=20, default='500g',null=True)
    class Meta:
        db_table='order_detail'


