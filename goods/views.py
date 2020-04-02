from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from goods.models import GoodsInfo, TypeInfo
from django.core import serializers


def goods_detail(request):
    id = request.GET.get('id')
    try:
        good_info = GoodsInfo.objects.get(id=id)
        good_info.gclick+=1
        good_info.save()

        name = good_info.gtype.title
    except:
        return HttpResponse("我们好像遇到一点问题了请稍后重试！")


    return render(request,'detail.html',locals())
# 商品推荐
def get_recommend1(request):

    gtype = request.GET.get('gtype')
    good_info = GoodsInfo.objects.filter(gtype_id=gtype)[0:2]

    str = serializers.serialize('json',good_info)

    return JsonResponse(str,safe=False)
#根据人气获取商品列表
def good_list(request):
    gtype = request.GET.get('type')
    gname= TypeInfo.objects.filter(id=gtype)[0]
    goods_info = GoodsInfo.objects.filter(gtype_id=gtype)
    paginator = Paginator(goods_info,15)
    cur_page = request.GET.get('page',1)
    page = paginator.page(cur_page)
    return render(request,'list.html',locals())
#根据价格获取商品列表
@csrf_exempt
def good_list1(request):
    gtype = request.GET.get('type')
    sign =request.GET.get('sign')

    gname = TypeInfo.objects.filter(id=gtype)[0]
    if(sign == '1'):
        goods_info = GoodsInfo.objects.filter(gtype_id=gtype).order_by('gprice')
    else:
        goods_info = GoodsInfo.objects.filter(gtype_id=gtype).order_by('-gprice')
    paginator = Paginator(goods_info, 15)
    cur_page = request.GET.get('page', 1)
    page = paginator.page(cur_page)
    return render(request, 'list.html', locals())
#商品搜索
def good_serch(request):

    if request.method == 'POST':
        val = request.POST.get('val')

        goods = GoodsInfo.objects.filter(gtitle__contains=val)
        types = TypeInfo.objects.filter(title__contains=val)

        if goods or types:
            result = {'code':200,'data':serializers.serialize('json',goods),'data1':serializers.serialize('json',types)}

        else:
            result = {'code':404}
        return JsonResponse(result)
    elif request.method == 'GET':
        val = request.GET.get('val')

        goods = GoodsInfo.objects.filter(gtitle__contains=val)
        types = TypeInfo.objects.filter(title__contains=val)
        if not goods and not types:
            result = None

        else:
            result = {'data':goods,'data1': types}
        print(result)

        return render(request,'search_lists.html',locals())



