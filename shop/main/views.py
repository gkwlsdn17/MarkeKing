import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .db.dao import *
import traceback

# Create your views here.
def index(request):
    content = {}
    try:
        try:
            user_id = request.session['markeking_shop_user_id']
            content['user_id'] = user_id
        except Exception as e:
            # print(e)
            pass
        dao = Dao()
        items = dao.getGoodsList()
        content['items'] = items

    except Exception as e:
        traceback.print_exc()
    
    return render(request, 'main/index.html', content)

def pageLogin(request):
    print(f"request.session:{request.session}")
    return render(request, 'main/login.html')

def login(request):
    try:
        id = request.POST.get('id')
        pw = request.POST.get('pw')

        dao = Dao()
        customer = dao.getCustomer(id)
        
        if customer.CUSTOMER_PW == pw:
            request.session['markeking_shop_user_id'] = id
            dao.updateCustomerLastVisit(customer.id)
            print('login success')
            return redirect("/")

        print('login fail')
        return redirect("pageLogin")

    except Exception as e: 
        # print(e)
        traceback.print_exc()
        return redirect("pageLogin")

def logout(request):
    try:
        id = request.session['markeking_shop_user_id']
        print(f'{id} delete')
        del request.session['markeking_shop_user_id']
    except Exception as e:
        print(e)
    
    return redirect("/")
    
def pageSignup(request):
    return render(request, 'main/signup.html')

def signup(request):
    try:
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        birth = request.POST.get('birth')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        zipcode = request.POST.get('zipcode')
        addr = request.POST.get('addr')
        sex = request.POST.get('sex') 
        
       
        dao = Dao()
        count = dao.getCustomerIdCount(id)
        if count == 0:
            res = dao.insertCustomer(id, pw, name, birth, phone, email, zipcode, addr, sex)
        else:
            print('exists')

    except Exception as e:
        traceback.print_exc()

    return redirect("/")

def pageOrder(request):
    content = {}
    goods = json.loads(request.POST.get('goods'))
    print(goods)
    content['goods'] = goods
    return render(request, 'main/order.html', content)

def orderSubmit(request):

    try:
        dname = request.POST.get('dname')
        daddr = request.POST.get('daddr')
        dphone = request.POST.get('dphone')
        items = json.loads(request.POST.get('items'))

        total_amount = 0
        for item in items:
            price = int(item['GOODS_COUNT']) * int(item['GOODS_PRICE'])
            item['TOTAL_AMOUNT'] = price
            total_amount += price

        today = datetime.now().strftime('%Y%m%d%H%M%S')

        user_id = request.session['markeking_shop_user_id']
        dao = Dao()
        cid = dao.getCustomerId(user_id)
        if cid != '':
            od = dao.insertOrder(cid, today, total_amount)
            if od:
                oid = dao.getOrderId(cid, today)
                if oid:
                    for item in items:
                        result = dao.insertItem(oid, item['GOODS_NO'], item['GOODS_NAME'], int(item['GOODS_COUNT']), int(item['GOODS_PRICE']), item['TOTAL_AMOUNT'])
                        if result == False:
                            raise Exception('item db insert fail')
                    
                    result = dao.insertDelivery(oid, cid, dname, daddr, dphone)
                    if result == False:
                        raise Exception('delivery db insert fail')

                    print(":::order submit success:::")
                else:
                    raise Exception('order id not find')
            else:
                raise Exception('order db insert fail')
        else:
            raise Exception('customer id not find')

    except Exception as e:
        print(e)
        traceback.print_exc()

    return redirect("/")