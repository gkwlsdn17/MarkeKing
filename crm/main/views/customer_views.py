from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from ..decorators import login_required
from ..models import *

@login_required
def selectCustomer(request):
    customer_list = Customer.objects.all()
    page = request.GET.get('page', '1')
    paginator = Paginator(customer_list, '10')
    page_obj = paginator.page(page)
    return render(request, 'main/customer.html', {'page_obj': page_obj})