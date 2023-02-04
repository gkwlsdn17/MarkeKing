from django.shortcuts import render, redirect
from ..decorators import login_required
import logging
import datetime
from ..models import *
from django.db.models import *
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

        content = {
            'weekStartDate': (today + relativedelta(days=-weekday)).strftime('%Y-%m-%d'),
            'weekEndDate': (today + relativedelta(days=7-1-weekday)).strftime('%Y-%m-%d'),
            'todayCount': todayCount, 'weekCount': weekCount, 'monthCount': monthCount,
            'todayOrderCount': todayOrderCount, 'weekOrderCount': weekOrderCount, 'monthOrderCount': monthOrderCount,
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