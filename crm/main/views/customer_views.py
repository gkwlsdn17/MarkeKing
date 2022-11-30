from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from ..decorators import login_required
from ..models import *
import datetime
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_datetime

@login_required
def selectCustomer(request):

    q = Q()
    search_all = request.GET.get('all', None)
    customer_name = request.GET.get('name', None)
    customer_id = request.GET.get('id', None)
    customer_birth = request.GET.get('birth', None)
    customer_phone = request.GET.get('phone', None)
    customer_email = request.GET.get('email', None)
    customer_addr = request.GET.get('addr', None)
    customer_rating = request.GET.get('rating', None)

    if search_all:
        q |= Q(CUSTOMER_NAME__contains = search_all)
        q |= Q(CUSTOMER_ID__contains = search_all)
        q |= Q(CUSTOMER_BIRTH__contains = search_all)
        q |= Q(CUSTOMER_PHONE__contains = search_all)
        q |= Q(CUSTOMER_EMAIL__contains = search_all)
        q |= Q(CUSTOMER_ADDR__contains = search_all)
        q |= Q(CUSTOMER_RATING__contains = search_all)
    if customer_name:
        q &= Q(CUSTOMER_NAME__contains = customer_name)
    if customer_id:
        q &= Q(CUSTOMER_ID__contains = customer_id)
    if customer_birth:
        q &= Q(CUSTOMER_BIRTH__contains = customer_birth)
    if customer_phone:
        q &= Q(CUSTOMER_PHONE__contains = customer_phone)
    if customer_email:
        q &= Q(CUSTOMER_EMAIL__contains = customer_email)
    if customer_addr:
        q &= Q(CUSTOMER_ADDR__contains = customer_addr)
    if customer_rating:
        q &= Q(CUSTOMER_RATING__NAME__icontains = customer_rating)

    q &= Q(DISCARD = False)

    customer_list = Customer.objects.all().filter(q) 
    page = request.GET.get('page', '1')
    paginator = Paginator(customer_list, '10')
    page_obj = paginator.page(page)
    
    return render(request, 'main/customer.html', {'page_obj': page_obj})

@login_required
def pageInsertCustomer(request):
    ratings = Rating.objects.all().filter(DISCARD=False)
    content = {'ratings': ratings}
    return render(request, 'main/customer_insert.html', content)

@login_required
def insertCustomer(request):
    try:
        id = request.POST.get('customer_id')
        pw = request.POST.get('customer_pw')
        name = request.POST.get('customer_name')
        birth = request.POST.get('customer_birth')
        phone = request.POST.get('customer_phone')
        email = request.POST.get('customer_email')
        addr = request.POST.get('customer_addr')
        visit_cnt = request.POST.get('visit_cnt')
        rating = request.POST.get('customer_rating')

        robj = Rating.objects.get(id = rating)

        customer = Customer(
            CUSTOMER_ID = id,
            CUSTOMER_PW = pw,
            CUSTOMER_NAME = name,
            CUSTOMER_BIRTH = birth,
            CUSTOMER_PHONE = phone,
            CUSTOMER_EMAIL = email,
            CUSTOMER_ADDR = addr,
            LAST_VISIT = datetime.datetime.now(),
            VISIT_CNT = visit_cnt,
            CUSTOMER_RATING = robj)

        print(customer)
        customer.save()
    except Exception as e:
        print(e)
    
    return redirect("customer_home")

@login_required
def pageCustomerDetail(request, customer_id):
    try:
        if customer_id is None:
            return redirect("customer_home")

        customer = Customer.objects.get(CUSTOMER_ID=customer_id)
        ratings = Rating.objects.all().filter(DISCARD = False)
        content = {'customer': customer, 'ratings': ratings}
        return render(request, 'main/customer_detail.html', content)
    except:
        return redirect("customer_home")

@login_required
def updateCustomer(request):
    try:
        id = request.POST.get('customer_id')
        name = request.POST.get('customer_name')    
        birth = request.POST.get('customer_birth')
        phone = request.POST.get('customer_phone')
        email = request.POST.get('customer_email')
        addr = request.POST.get('customer_addr')
        rating = request.POST.get('customer_rating')

        robj = Rating.objects.get(id = rating)
        customer = Customer.objects.get(CUSTOMER_ID = id)
        customer.CUSTOMER_NAME = name
        customer.CUSTOMER_BIRTH = birth
        customer.CUSTOMER_PHONE = phone
        customer.CUSTOMER_EMAIL = email
        customer.CUSTOMER_ADDR = addr
        customer.CUSTOMER_RATING = robj
        customer.save()
        return redirect("customer_home")
    except:
        redirect('customer_detail', customer_id=id)

@login_required
def deleteCustomer(request, cid):
    try:
        customer = Customer.objects.get(id = cid)
        customer.DISCARD = True
        customer.save()
        return redirect("customer_home")
    except:
       return redirect('customer_detail', customer_id=cid)
    
@login_required
def pageCustomerDetailSearch(request):

    q = Q()
    customer_name = request.GET.get('name', None)
    customer_id = request.GET.get('id', None)
    s_age = request.GET.get('s_age', None)
    e_age = request.GET.get('e_age', None)
    customer_phone = request.GET.get('phone', None)
    customer_email = request.GET.get('email', None)
    customer_addr = request.GET.get('addr', None)
    customer_rating = request.GET.get('rating', None)
    s_visit = request.GET.get('s_visit', None)
    e_visit = request.GET.get('e_visit', None)
    s_cnt = request.GET.get('s_cnt', None)
    e_cnt = request.GET.get('e_cnt', None)

    if customer_name:
        q &= Q(CUSTOMER_NAME__contains = customer_name)
    if customer_id:
        q &= Q(CUSTOMER_ID__contains = customer_id)
    if s_age and e_age:
        s_year = (datetime.datetime.now() - relativedelta(years=int(s_age)-1)).year
        e_year = (datetime.datetime.now() - relativedelta(years=int(e_age)-1)).year
        if e_year < s_year:
            s_year , e_year = e_year , s_year
        q &= Q(CUSTOMER_BIRTH__range=(f'{s_year}0101', f'{e_year+1}0101'))
    if customer_phone:
        q &= Q(CUSTOMER_PHONE__contains = customer_phone)
    if customer_email:
        q &= Q(CUSTOMER_EMAIL__contains = customer_email)
    if customer_addr:
        q &= Q(CUSTOMER_ADDR__contains = customer_addr)
    if customer_rating:
        q &= Q(CUSTOMER_RATING__contains = customer_rating)
    if s_visit and e_visit:
        if e_visit < s_visit:
            s_visit , e_visit = e_visit , s_visit
        
        s_visit = parse_datetime(s_visit)
        e_visit = parse_datetime(e_visit)
        e_visit = e_visit + relativedelta(days=1)
        q &= Q(LAST_VISIT__range=(s_visit,e_visit))
    if s_cnt and e_cnt:
        if e_cnt < s_cnt:
            s_cnt , e_cnt = e_cnt , s_cnt
        print(s_cnt, e_cnt)
        q &= Q(VISIT_CNT__range=(s_cnt, e_cnt))

    q &= Q(DISCARD = False)

    customer_list = Customer.objects.all().filter(q) 
    page = request.GET.get('page', '1')
    paginator = Paginator(customer_list, '10')
    page_obj = paginator.page(page)

    return render(request, 'main/customer_detail_search.html', {'page_obj': page_obj})