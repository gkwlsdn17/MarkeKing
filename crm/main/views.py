from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html')
    else:
        return redirect('login_home')

def selectCustomer(request):
    return render(request, 'main/customer.html')