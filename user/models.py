from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30,unique=True)
    pwd = models.CharField(max_length=64)
    email = models.CharField(max_length=30,unique=True)
class Address(models.Model):
    user_id = models.ForeignKey(User)
    re_name = models.CharField(max_length=20)
    detail_info = models.CharField(max_length=50)
    postcode = models.IntegerField()
    phone_num = models.CharField(max_length=20)




