from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Rating)
admin.site.register(Goods)
admin.site.register(GoodsType)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(DeliveryStatus)
admin.site.register(DeliveryCompany)
