from django.shortcuts import render, redirect
from django.db.models import *
from django.core.paginator import Paginator
from django.db.models.functions import RowNumber
from dateutil.relativedelta import relativedelta
from ..decorators import login_required
import datetime
from ..models import *
import logging
logger = logging.getLogger('sales')

@login_required
def pageSalesMain(request):
    return render(request, 'main/sales_main.html')

@login_required
def pageSalesList(request):
    searchQuery = ""
    try:
        startDate = request.GET.get('startDate', None)
        endDate = request.GET.get('endDate', None)

        today = datetime.datetime.now()

        if startDate is None:
            startDate = today.strftime('%Y%m')
            startDate += '01'
        if endDate is None:
            end = today + relativedelta(days=1)
            endDate = end.strftime('%Y%m%d')
        print(startDate, endDate)
        q = Q()
        q &= Q(ORDER_DATE__range=(startDate, endDate))
        q &= Q(DISCARD = False)

        sales_list = Order.objects.all().annotate(
            row = Window(expression=RowNumber(), order_by=F('id').asc())
        ).filter(q).order_by('-row')
        
        page = request.GET.get('page', '1')
        paginator = Paginator(sales_list, '10')
        page_obj = paginator.page(page)
        return render(request, 'main/sales_list.html',{'page_obj': page_obj, 'startDate': startDate, 'endDate': endDate})
    except Exception as e:
        logger.error(e)
        return render(request, 'main/error.html')
    
    
@login_required
def pageSalesDetail(request, order_id):
    try:
        order = Order.objects.get(id = order_id)
        items = Item.objects.all().filter(ORDER_NO = order_id)
        delivery = Delivery.objects.filter(ORDER_NO = order_id)

        return render(request, 'main/sales_detail.html', {'order': order, 'items': items, 'delivery': delivery})
    except Exception as e:
        logger.error(e)
        return render(request, 'main/error.html')