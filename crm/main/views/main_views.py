from django.shortcuts import render, redirect
from ..decorators import login_required

@login_required
def index(request):
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html')
    else:
        return redirect('login_home')
