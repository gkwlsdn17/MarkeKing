from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import logging
logger = logging.getLogger('login')


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
            request.session['user_id'] = user_id
            logger.info(f'{user.USER_ID} LOGIN')
            return redirect('/')
    except Exception as e:
        logger.error(e)
        return redirect('login_home')

    

def logout(request):
    try:
        id = request.session['user_id']
        del request.session['user_name']
        del request.session['user_id']
        logger.info(f'{id} LOGOUT')
    except Exception as e:
        logger.error(e)

    return redirect('login_home')

def page_signIn(request):
    return render(request, 'login/signIn.html')

def signIn(request):
    try:
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_name = request.POST['user_name']
        user_birth = request.POST['user_birth']
        user_phone = request.POST['user_phone']
        user_email = request.POST['user_email']

        try:
            user = User.objects.get(USER_ID = user_id)
        except User.DoesNotExist:
            user = User(
                USER_ID = user_id,
                USER_PW = user_pw,
                USER_NAME = user_name,
                USER_BIRTH = user_birth,
                USER_PHONE = user_phone,
                USER_EMAIL = user_email
                )
            user.save()
            logger.info(f'{user_id} SIGN IN SUCCESS')
            # messages.success(request, '회원가입에 성공하였습니다.')
            # return render(request, 'login/login.html')
            return redirect('login_home')

        # messages.error(request, '회원가입에 실패했습니다.')
        # return render(request, 'login/signIn.html')
        return redirect('page_signIn')
        

    except Exception as e:
        logger.error(e)
        # messages.error(request, '회원가입에 실패했습니다.')
        # return render(request, 'login/signIn.html')
        return redirect('page_signIn')