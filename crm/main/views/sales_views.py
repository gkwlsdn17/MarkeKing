from django.shortcuts import render, redirect
from django.db.models import *
from django.core.paginator import Paginator
from django.db.models.functions import RowNumber
from dateutil.relativedelta import relativedelta
from ..decorators import login_required
import datetime
from ..models import *
import traceback
import logging
logger = logging.getLogger('sales')

@login_required
def pageSalesMain(request):
    content = {}
    try:
        #(start.strftime('%Y-%m-%d'), (today + relativedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.datetime.today()
        weekday = today.weekday()

        # 이번주 월 ~ 일까지 데이터 구함
        startDate = (today + relativedelta(days=-weekday)).strftime('%Y%m%d')
        endDate = (today + relativedelta(days=7-weekday)).strftime('%Y%m%d')
        content['startDate'] = startDate
        content['endDate'] = endDate

        q = Q()
        q &= Q(ORDER_DATE__range=(startDate, endDate))
        q &= Q(DISCARD = False)

        weekSalesCnt = Order.objects.all().filter(q).count()
        weekSalesSum = Order.objects.all().filter(q).aggregate(sum = Sum('TOTAL_AMOUNT'))['sum'] or 0
        content['weekSalesCnt'] = weekSalesCnt
        content['weekSalesSum'] = weekSalesSum

        cntTopList = getOrderCntTopList(q, 5)
        if cntTopList:
            content['cntTopList'] = cntTopList
            if cntTopList.count != 5:
                content['cntTopList_blank'] = [0 for i in range(5-cntTopList.count())]

        amtTopList = getOrderAmtTopList(q, 5)
        if amtTopList:
            content['amtTopList'] = amtTopList    
            if amtTopList.count != 5:
                content['amtTopList_blank'] = [0 for i in range(5-amtTopList.count())]

        # for i in cntTopList:
        #     print(i)
        # for i in amtTopList:
        #     print(i)
        
        q2 = Q(ORDER_NO__DISCARD=False)
        q2 &= Q(ORDER_NO__ORDER_DATE__range=(startDate, endDate))

        itemList = getItemTopList(q2 ,5)
        if itemList:
            content['itemList'] = itemList
            if itemList.count != 5:
                content['itemList_blank'] = [0 for i in range(5-itemList.count())]


        deliveryList = getDeliveryStatus(q2)
        statusList = getStatusList()
        slist = []
        for status in statusList:
            item = next((item for item in deliveryList if item.get('DELIVERY_STATUS_id') == status.id),None)
            if item is None:
                slist.append({'Delivery_status_id': status.id, 'DELIVERY_STATUS__STATUS': status.STATUS, 'cnt': 0})
            else:
                slist.append(item)
        
        if deliveryList:
            content['deliveryList'] = slist

        
    except Exception as e:
        logger.error(e)
        
    return render(request, 'main/sales_main.html', content)

def getOrderCntTopList(q, limit):
    try:
        # 주문횟수 top
        cntTopList = Order.objects.all().filter(q).values('CUSTOMER_NO__CUSTOMER_ID').annotate(
            cnt = Count('CUSTOMER_NO__CUSTOMER_ID'),
            row = Window(expression=RowNumber(), order_by=F('cnt').desc()),
        ).values('row', 'cnt', 'CUSTOMER_NO__CUSTOMER_ID').order_by('-cnt')[:limit]
        return cntTopList
    except Exception as e:
        logger.error(e)
        return None

def getOrderAmtTopList(q, limit):
    try:
        # 주문금액 top
        amtTopList = Order.objects.all().filter(q).values('CUSTOMER_NO__CUSTOMER_ID', 'TOTAL_AMOUNT').annotate(
            row = Window(expression=RowNumber(), order_by=F('TOTAL_AMOUNT').desc()),
        ).order_by('row')[:limit]
        return amtTopList
    except Exception as e:
        logger.error(e)
        return None

def getItemTopList(q, limit):
    try:
        itemList = Item.objects.all().filter(q).values('GOODS_NO__id', 'GOODS_NAME', 'GOODS_COUNT').annotate(
            cnt = Count('GOODS_NO__id'),
            count = Sum('GOODS_COUNT'),
            row = Window(expression=RowNumber(), order_by=F('cnt').desc()),
        ).values('cnt','GOODS_NAME','count','row').order_by('-cnt')[:limit]
        return itemList
    except Exception as e:
        logger.error(e)
        return None

def getDeliveryStatus(q):
    try:
        list = Delivery.objects.all().filter(q).values('DELIVERY_STATUS_id', 'DELIVERY_STATUS__STATUS').annotate(
            cnt = Count('DELIVERY_STATUS_id')).values(
            'cnt', 'DELIVERY_STATUS_id', 'DELIVERY_STATUS__STATUS').order_by('DELIVERY_STATUS_id')
        
        return list
    except Exception as e:
        logger.error(e)
        return None

def getStatusList():
    try:
        # list = DeliveryStatus.objects.all().filter(q).values('DELIVERY_STATUS_id', 'DELIVERY_STATUS__STATUS').annotate(
        #     cnt = Count('DELIVERY_STATUS_id')).values(
        #     'cnt', 'DELIVERY_STATUS_id', 'DELIVERY_STATUS__STATUS').order_by('DELIVERY_STATUS_id')

        list = DeliveryStatus.objects.all().filter(DISCARD=False)
        return list
    except Exception as e:
        logger.error(e)
        return None

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
        items = Item.objects.all().annotate(
            row = Window(expression=RowNumber(), order_by=F('id').asc()),
            ).filter(ORDER_NO = order_id)
        delivery = Delivery.objects.get(ORDER_NO = order_id)
        page = request.GET.get('page', '1')
        site = request.GET.get('site', '')
        print(delivery)
        content = {'order': order, 'items': items, 'delivery': delivery, 'page': page, 'site': site}
        
        return render(request, 'main/sales_detail.html', content)
    except Exception as e:
        logger.error(e)
        return render(request, 'main/error.html')

@login_required
def pageDeliveryList(request):
    try:
        startDate = request.GET.get('startDate', None)
        endDate = request.GET.get('endDate', None)
        arrivalStart = request.GET.get('arrivalStart', None)
        arrivalEnd = request.GET.get('arrivalEnd', None)

        pageType = request.GET.get('type', 'B')

        today = datetime.datetime.now()

        if startDate is None:
            startDate = today.strftime('%Y%m')
            startDate += '01'
        if endDate is None:
            end = today + relativedelta(days=1)
            endDate = end.strftime('%Y%m%d')

        q = Q()
        q &= Q(DISCARD = False)

        if pageType == 'B':
            q &= (Q(DELIVERY_DATE = '') | Q(DELIVERY_DATE__isnull=True))

            delivery_list = Delivery.objects.all().annotate(
            row = Window(expression=RowNumber(), order_by=F('id').asc()),
            ).filter(q).order_by('-row')
            
        
        else:
            q &= Q(DELIVERY_DATE__range=(startDate, endDate))
            delivery_list = Delivery.objects.all().annotate(
                row = Window(expression=RowNumber(), order_by=F('id').asc())
            ).filter(q).order_by('-row')
        
        page = request.GET.get('page', '1')
        paginator = Paginator(delivery_list, '10')
        page_obj = paginator.page(page)

        content = {'page_obj': page_obj, 'startDate': startDate, 'endDate': endDate, 'pageType': pageType}
        return render(request, 'main/sales_delivery_list.html', content)
    except Exception as e:
        logger.error(e)
        return render(request, 'main/error.html')

# 주문취소
@login_required
def salesCancel(request, order_id):
    try:
        delivery = Delivery.objects.get(ORDER_NO=order_id)
        items = Item.objects.filter(ORDER_NO=order_id)
        order = Order.objects.get(id = order_id)

        delivery.DISCARD = True
        delivery.save()
        logger.info(f'Delivery {delivery.id} DISCARD Success (Order ID: {order_id})')
        for item in items:
            item_id = item.id
            item.DISCARD = True
            logger.info(f'Item {item_id} DISCARD Success (Order ID: {order_id})')
        
        
        order.DISCARD = True
        order.CANCEL_DATE = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        order.save()
        logger.info(f'Order {order_id} DISCARD Success')
        
        return redirect('pageSalesCancelList')
    except Exception as e:
        logger.error(e)
        return render(request, 'main/error.html')

# 주문취소내역
@login_required
def pageSalesCancelList(request):
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
        
        q = Q()
        q &= Q(ORDER_DATE__range=(startDate, endDate))
        q &= Q(DISCARD = True)

        sales_list = Order.objects.all().annotate(
            row = Window(expression=RowNumber(), order_by=F('id').asc())
        ).filter(q).order_by('-row')
        
        page = request.GET.get('page', '1')
        paginator = Paginator(sales_list, '10')
        page_obj = paginator.page(page)
        return render(request, 'main/sales_cancel_list.html',{'page_obj': page_obj, 'startDate': startDate, 'endDate': endDate})
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return render(request, 'main/error.html')

# 주문취소상세내역
@login_required
def pageSalesCancelDetail(request, order_id):
    try:
        order = Order.objects.get(id = order_id)
        items = Item.objects.all().annotate(
            row = Window(expression=RowNumber(), order_by=F('id').asc()),
            ).filter(ORDER_NO = order_id)
        
        page = request.GET.get('page', '1')
        content = {'order': order, 'items': items, 'page': page}
        
        return render(request, 'main/sales_cancel_detail.html', content)
    except Exception as e:
        logger.error(traceback.print_exc())
        return render(request, 'main/error.html')