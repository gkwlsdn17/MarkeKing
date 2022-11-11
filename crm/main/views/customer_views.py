from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from ..decorators import login_required
from ..models import *
import datetime

@login_required
def selectCustomer(request):
    customer_list = Customer.objects.all()    
    page = request.GET.get('page', '1')
    paginator = Paginator(customer_list, '2')
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