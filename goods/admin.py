from django.contrib import admin
from . import models
# Register your models here.
class Type_Manage(admin.ModelAdmin):
    list_display = ['id','title','isDelete']
class Goods_Manage(admin.ModelAdmin):
    list_display = ['id','gtitle','gprice']
    list_display_links = ['id']

admin.site.register(models.TypeInfo,Type_Manage)
admin.site.register(models.GoodsInfo,Goods_Manage)
