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

        q &= Q(DISCARD = False)

        goods_list = Goods.objects.all().filter(q)
        page = request.GET.get('page', '1')
        paginator = Paginator(goods_list, '10')
        page_obj = paginator.page(page)

    except Exception as e:
        print(e)
        page_obj = {}

    return render(request, 'main/goods_main.html', {'page_obj': page_obj, 'types': types})

@login_required
def insertGoods(request):
    return render(request, 'goods_insert.html')