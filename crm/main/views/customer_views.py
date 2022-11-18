from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from ..decorators import login_required
from ..models import *
import datetime

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
        q &= Q(CUSTOMER_RATING__contains = customer_rating)

    q &= Q(DISCARD = False)

    customer_list = Customer.objects.all().filter(q) 
    page = request.GET.get('page', '1')
    paginator = Paginator(customer_list, '10')
    page_obj = paginator.page(page)
    
    return render(request, 'main/customer.html', {'page_obj': page_obj})

@login_required
def pageInsertCustomer(request):
    return render(request, 'main/customer_insert.html')

@login_required
def insertCustomer(request):
    id = request.POST.get('customer_id')
    pw = request.POST.get('customer_pw')
    name = request.POST.get('customer_name')
    birth = request.POST.get('customer_birth')
    phone = request.POST.get('customer_phone')
    email = request.POST.get('customer_email')
    addr = request.POST.get('customer_addr')
    visit_cnt = request.POST.get('visit_cnt')
    rating = request.POST.get('customer_rating')

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
        CUSTOMER_RATING = rating)

    print(customer)
    customer.save()
    
    return redirect("customer_home")

@login_required
def pageCustomerDetail(request, customer_id):
    try:
        if customer_id is None:
            return redirect("customer_home")

        customer = Customer.objects.get(CUSTOMER_ID=customer_id)
        content = {'customer': customer}
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
        customer = Customer.objects.get(CUSTOMER_ID = id)
        customer.CUSTOMER_NAME = name
        customer.CUSTOMER_BIRTH = birth
        customer.CUSTOMER_PHONE = phone
        customer.CUSTOMER_EMAIL = email
        customer.CUSTOMER_ADDR = addr
        customer.CUSTOMER_RATING = rating
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
    


def searchCondition(condition):
    return "CUSTOMER_" + condition
    