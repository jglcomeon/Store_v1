from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30,unique=True)
    pwd = models.CharField(max_length=64)
    email = models.CharField(max_length=30,unique=True)