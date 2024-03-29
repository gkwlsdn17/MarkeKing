import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import *
from django.db.models.functions import Substr
from ..decorators import login_required
from ..models import *
import datetime
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_datetime
import logging
import traceback
logger = logging.getLogger('goods')

@login_required
def pageGoodsMain(request):
    try: 
        types = GoodsType.objects.all().filter(DISCARD=0)

        q = Q()
        search_all = request.GET.get('all', None)
        name = request.GET.get('name', None)
        type = request.GET.get('type', None)
        barcode = request.GET.get('barcode', None)
        price = request.GET.get('price', None)
        tid = request.GET.get('tid', None)

        if search_all:
            q |= Q(NAME__contains = search_all)
            q |= Q(TYPE__NAME__icontains = search_all)
            q |= Q(BARCODE__contains = search_all)
            q |= Q(PRICE__contains = search_all)
            
        if name:
            q &= Q(NAME__contains = name)
        if type:
            q &= Q(TYPE__NAME__icontains = type)
        if barcode:
            q &= Q(BARCODE__contains = barcode)
        if price:
            q &= Q(PRICE__contains = price)
        if tid:
            q &= Q(TYPE = tid)

        q &= Q(DISCARD = False)

        goods_list = Goods.objects.all().filter(q).order_by('-id')
        page = request.GET.get('page', '1')
        paginator = Paginator(goods_list, '10')
        page_obj = paginator.page(page)

    except Exception as e:
        logger.error(e)
        page_obj = {}

    return render(request, 'main/goods_main.html', {'page_obj': page_obj, 'types': types})

@login_required
def pageInsertGoods(request):
    context = {}
    try:
        types = GoodsType.objects.all().filter(DISCARD=False)
        context['types'] = types
    except Exception as e:
        logger.error(e)

    return render(request, 'main/goods_insert.html', {'types': types})

@login_required
def insertGoods(request):
    
    try:
        name = request.POST.get('goods_name',None)
        type = request.POST.get('goods_type',None)
        barcode = request.POST.get('goods_barcode',None)
        price = request.POST.get('goods_price',None)
        
        goods_type = GoodsType.objects.get(id = type)

        goods = Goods(
            NAME = name,
            TYPE = goods_type,
            BARCODE = barcode,
            PRICE = price
        )

        goods.save()
        logger.info(f'insertGoods - {name} Save')
        return redirect('pageGoodsMain')
    
    except Exception as e:
        logger.error(e)
        return render(request, 'main/goods_insert.html')
    
@login_required
def goodsDetail(request , goods_id):
    try:
        if goods_id is None:
            return redirect("pageGoodsMain")

        goods = Goods.objects.get(id = goods_id)
        
        goods_type = GoodsType.objects.all().filter(DISCARD=False)
        context = {'goods': goods, 'types': goods_type}
        return render(request, 'main/goods_detail.html', context)
    except Exception as e:
        logger.error(e)
        return redirect('pageGoodsMain')

@login_required
def updateGoods(request):
    try:
        id = request.POST.get('goods_id')
        name = request.POST.get('goods_name')
        type = request.POST.get('goods_type')
        barcode = request.POST.get('goods_barcode')
        goods_price = request.POST.get('goods_price')
        goods_image = request.FILES.get('goods_image')

        print(f'goods_image: {goods_image}')
        
        goodsType = GoodsType.objects.get(id= type)

        goods = Goods.objects.get(id = id)
        goods.NAME = name
        goods.TYPE = goodsType
        goods.BARCODE = barcode
        goods.PRICE = goods_price

        if goods_image:
            image = GoodsImage(
                IMAGE_PATH = goods_image
            )
            print(image)
            image.save()
            if goods.IMAGE:
                existImage = GoodsImage.objects.get(id = goods.IMAGE.id)
                existImage.DISCARD = True
                existImage.save()

            image = GoodsImage.objects.get(IMAGE_PATH = image.IMAGE_PATH, DISCARD = False)
            goods.IMAGE = image

        goods.save()
        logger.info(f'UpdateGoods - {id} Update')
        return redirect('pageGoodsMain')

    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return redirect('pageGoodsMain')

@login_required
def deleteGoods(request, gid):
    try:
        goods = Goods.objects.get(id = gid)
        goods.DISCARD = True
        goods.save()
        logger.info(f'DeleteGoods - {gid} Delete')
        return redirect('pageGoodsMain')
    except Exception as e:
        logger.error(e)
        return redirect('pageGoodsMain')