from django.shortcuts import render, redirect
from ..decorators import login_required
from ..models import *

@login_required
def pageSetup(request):
    try:
        ratings = Rating.objects.all().filter(DISCARD=False).order_by('ORDER')
        content = {'ratings': ratings}
    except:
        ratings = []
    return render(request, 'main/setup.html', content)

@login_required
def insertRating(request):
    try:
        name = request.GET.get('name',None)
        order = request.GET.get('order',None)
        obj = Rating(
            NAME = name,
            ORDER = order
        )
        obj.save()
    except Exception as e:
        print(e)
        
    return redirect('pageSetup')

@login_required
def updateRating(request):
    try:
        id = request.POST.get('td_rating_id')
        name = request.POST.get('td_rating_name')
        order = request.POST.get('td_rating_order')
        obj = Rating.objects.get(id = id)
        obj.NAME = name
        obj.ORDER = order
        obj.save()
    except Exception as e:
        print(e)
    return redirect('pageSetup')

@login_required
def deleteRating(request, id):
    try:
        obj = Rating.objects.get(id = id)
        obj.DISCARD = True
        obj.save()
    except Exception as e:
        print(e)
    return redirect('pageSetup')