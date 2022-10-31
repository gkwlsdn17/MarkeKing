from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def login_home(request):
    return render(request, 'login/login.html')

def login(request):

    user_id = request.POST['user_id']
    user_pw = request.POST['user_pw']
    try:
        user = User.objects.get(USER_ID = user_id)
        if user.USER_PW == user_pw:
            request.session['user_name'] = user.USER_NAME
            return redirect('/')
    except:
        return redirect('login_home')

    

def logout(request):
    del request.session['user_name']
    return redirect('login_home')
