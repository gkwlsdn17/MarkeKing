from django.urls import path
from .views import main_views, customer_views

urlpatterns = [
    path('', main_views.index),
    path('customer/', customer_views.selectCustomer, name="customer_home"),
    path('customer/insert/' , customer_views.insertCustomer),
    path('customer/insert/view/', customer_views.pageInsertCustomer),
    
    

]