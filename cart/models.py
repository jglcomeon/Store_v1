from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey('user.User',null=True)
    good = models.ForeignKey('goods.GoodsInfo',null=True)
    num = models.IntegerField()
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    gunit = models.CharField(max_length=20, default='500g')
    sum = models.DecimalField(max_digits=10,decimal_places=2)
