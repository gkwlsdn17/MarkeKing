from django.shortcuts import render, redirect
from ..decorators import login_required
import logging
import datetime
from ..models import *
from django.db.models import *
from django.db.models.functions import RowNumber
from dateutil.relativedelta import relativedelta
logger = logging.getLogger('main')

@login_required
def index(request):
    if 'user_name' in request.session.keys():
        
        today = datetime.datetime.today()
        weekday = today.weekday()

        # 회원방문횟수
        todayCount = visitCount(today.strftime('%Y-%m-%d'), (today + relativedelta(days=1)).strftime('%Y-%m-%d'))
        weekCount = visitCount((today + relativedelta(days=-weekday)).strftime('%Y-%m-%d'), (today + relativedelta(days=7-weekday)).strftime('%Y-%m-%d'))
        monthCount = visitCount(today.strftime('%Y-%m-')+"01", (today + relativedelta(days=1)).strftime('%Y-%m-%d'))

        # 주문건수
        
        todayOrderCount = orderCount(today.strftime('%Y%m%d'+"000000"), (today + relativedelta(days=1)).strftime('%Y%m%d%H%M%S'))
        weekOrderCount = orderCount((today + relativedelta(days=-weekday)).strftime('%Y%m%d'+"000000"), (today + relativedelta(days=7-weekday)).strftime('%Y%m%d%H%M%S'))
        monthOrderCount = orderCount(today.strftime('%Y%m')+"01000000", (today + relativedelta(days=1)).strftime('%Y%m%d%H%M%S'))


        # 주문진행중
        orderList = orderStatus()
        
        # 회원가입 숫자
        customerCnt = customerStatus()
        print(customerCnt)

        content = {
            'weekStartDate': (today + relativedelta(days=-weekday)).strftime('%Y-%m-%d'),
            'weekEndDate': (today + relativedelta(days=7-1-weekday)).strftime('%Y-%m-%d'),
            'todayCount': todayCount, 'weekCount': weekCount, 'monthCount': monthCount,
            'todayOrderCount': todayOrderCount, 'weekOrderCount': weekOrderCount, 'monthOrderCount': monthOrderCount,
            'orderList': orderList, 'customerCnt': customerCnt,
            }
        return render(request, 'main/index.html', content)
    else:
        return redirect('login_home')

# 회원방문횟수
def visitCount(startDate, endDate):
    try:
        q = Q()
        q &= Q(DISCARD = False)
        q &= Q(LAST_VISIT__range=(startDate, endDate))

        count = Customer.objects.filter(q).count()
        return count
    except Exception as e:
        logger.error(e)
        return 0

# 주문건수
def orderCount(startDate, endDate):
    try:
        q = Q()
        q &= Q(DISCARD = False)
        q &= Q(ORDER_DATE__range=(startDate, endDate))

        count = Order.objects.filter(q).count()
        return count
    except Exception as e:
        logger.error(e)
        return 0

# 주문진행중
def orderStatus():
    try:
        q = Q()
        q &= Q(DISCARD = False)
        q &= Q(DELIVERY_STATUS_id__lt = 4)

        list = Delivery.objects.filter(q).values('CUSTOMER_NO__CUSTOMER_ID', 'CUSTOMER_NO__CUSTOMER_NAME', 'DELIVERY_STATUS__STATUS', 'id').annotate(
            row = Window(expression=RowNumber(), order_by=F('id').desc())
        ).order_by('row')[:5]
        return list
    except Exception as e:
        logger.error(e)
        return None

def customerStatus():
    try:
        q = Q()
        q &= Q(DISCARD = False)

        allCnt = Customer.objects.filter(q).count()

        today = datetime.datetime.today()
        start = today + relativedelta(days=-6)

        q &= Q(FIRST_VISIT__range=(start.strftime('%Y-%m-%d'), (today + relativedelta(days=1)).strftime('%Y-%m-%d')))
        weekCnt = Customer.objects.filter(q).count()
        todayCnt = Customer.objects.all().filter(FIRST_VISIT__range=(today, (today + relativedelta(days=1)).strftime('%Y-%m-%d'))).count()

        content = {
            'allCnt': allCnt,
            'weekCnt': weekCnt,
            'todayCnt': todayCnt
        }

        return content
    except Exception as e:
        logger.error(e)
        return None