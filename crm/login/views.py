from django.shortcuts import render, redirect


# Create your views here.

def login_home(request):
    return render(request, 'login/login.html')

def login(request):
    request.session['user_name'] = '권희경'
    return redirect('/')

def logout(request):
    del request.session['user_name']
    return redirect('login_home')
