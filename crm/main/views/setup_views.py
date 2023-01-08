from django.shortcuts import render, redirect
from ..decorators import login_required
from ..models import *
import logging
logger = logging.getLogger('setup')

@login_required
def pageSetup(request):
    try:
        ratings = Rating.objects.all().filter(DISCARD=False).order_by('ORDER')
        goods_types = GoodsType.objects.all().filter(DISCARD=False)

        content = {
            'ratings': ratings,
            'goods_types' : goods_types
        }
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
        logger.info(f'Setting Rating - {name} Save')
    except Exception as e:
        logger.error(e)
        
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
        logger.info(f'Setting Rating - {id} Update')
    except Exception as e:
        logger.error(e)
    return redirect('pageSetup')

@login_required
def deleteRating(request, id):
    try:
        obj = Rating.objects.get(id = id)
        obj.DISCARD = True
        obj.save()
        logger.info(f'Setting Rating {id} Delete')
    except Exception as e:
        logger.error(e)
    return redirect('pageSetup')

@login_required
def insertGoodsType(request):
    try:
        name = request.GET.get('name',None)
        obj = GoodsType(
            NAME = name,
        )
        obj.save()
        logger.info(f'Setting GoodsType - {name} Save')
    except Exception as e:
        logger.error(e)
        
    return redirect('pageSetup')

@login_required
def deleteGoodsType(request, id):
    try:
        obj = GoodsType.objects.get(id = id)
        obj.DISCARD = True
        obj.save()
        logger.info(f'Setting GoodsType - {id} Delete')
    except Exception as e:
        logger.error(e)
    return redirect('pageSetup')


