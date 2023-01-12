import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def index(request):
    content = {}
    try:
        c = connection.cursor()
        query = f'''
        SELECT main_goods.id, main_goods.NAME, main_goods.PRICE, main_goodstype.NAME
        FROM main_goods join main_goodstype
        ON main_goods.TYPE_id = main_goodstype.id
        ORDER BY main_goods.id DESC LIMIT 10
        '''
        
        res = c.execute(query)
        items = c.fetchall()
        for i in items:
            print(i)

        content['items'] = items

    except Exception as e:
        print(e)
    finally:
        connection.close()
    
    print(content)
    return render(request, 'main/index.html', content)

def login(request):
    return render(request, 'main/login.html')

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

        if sex == '남':
            sex = 1
        elif sex == '여':
            sex = 2
        else:
            sex = 0
        
        c = connection.cursor()

        query = f"SELECT COUNT(*) FROM main_customer WHERE CUSTOMER_ID = '{id}'"
        res = c.execute(query)
        rows = res.fetchone()
        connection.commit()
        print(f'res = {res}')
        if rows[0] == 0:
            query = f'''
            INSERT INTO main_customer(CUSTOMER_ID, CUSTOMER_PW, CUSTOMER_NAME, CUSTOMER_BIRTH, CUSTOMER_PHONE, CUSTOMER_EMAIL, CUSTOMER_ZIPCODE, CUSTOMER_ADDR, CUSTOMER_SEX)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, {sex});
            '''
            c.execute(query, (id, pw, name, birth, phone, email, zipcode, addr))
            connection.commit()

            print('save ok')

        else:
            print('exists')


    except Exception as e:
        print(e)
    finally:
        connection.close()

    return render(request, 'main/signup.html')

def pageOrder(request):
    content = {}
    goods = json.loads(request.POST.get('goods'))
    content['goods'] = goods
    print(content)
    return render(request, 'main/order.html', content)

def orderSubmit(request):

    try:
        dname = request.POST.get('dname')
        daddr = request.POST.get('daddr')
        dphone = request.POST.get('dphone')
        items = json.loads(request.POST.get('items'))

        for item in items:
            print(item)

        # today = datetime.datetime.now().strftime('%Y%m%d')
        # print(today)
        # user_id = request.session['user_id']
        # query = f"SELECT id FROM main_customer WHERE id = {user_id}"
        # cursor = connection.cursor()
        # cursor.execute(query)
        # res = cursor.fetchone()
        # id = res[0]
        # query = F'''INSERT INTO main_order(CUSTOMER_NO, ORDER_DATE, TOTAL_AMOUNT, MEMO, CRTIME, DISCARD) 
        # VALUES({id}, '{today}', );
        # '''
    except Exception as e:
        print(e)

    return redirect("/")