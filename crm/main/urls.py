from django.urls import path
from .views import main_views, customer_views

urlpatterns = [
    path('', main_views.index),
    path('customer/', customer_views.selectCustomer, name="customer_home"),
    path('customer/insert/' , customer_views.insertCustomer, name="customer_insert"),
    path('customer/insert/view/', customer_views.pageInsertCustomer, name="customer_insert_view"),
    path('customer/detail/<str:customer_id>', customer_views.pageCustomerDetail, name="customer_detail"),
    path('customer/update/', customer_views.updateCustomer, name="customer_update"),
    path('customer/delete/<int:cid>', customer_views.deleteCustomer, name="customer_delete"),
    path('customer/search/detail', customer_views.pageCustomerDetailSearch, name="customer_detail_search"),
    
]