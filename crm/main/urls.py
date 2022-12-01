from django.urls import path
from .views import main_views, customer_views, setup_views

urlpatterns = [
    path('', main_views.index),
    path('customer/', customer_views.selectCustomer, name="customer_home"),
    path('customer/insert/' , customer_views.insertCustomer, name="customer_insert"),
    path('customer/insert/view/', customer_views.pageInsertCustomer, name="customer_insert_view"),
    path('customer/detail/<str:customer_id>', customer_views.pageCustomerDetail, name="customer_detail"),
    path('customer/update/', customer_views.updateCustomer, name="customer_update"),
    path('customer/delete/<int:cid>', customer_views.deleteCustomer, name="customer_delete"),
    path('customer/search/detail', customer_views.pageCustomerDetailSearch, name="customer_detail_search"),
    path('customer/statistics/', customer_views.pageStatistics, name="page_statistics"),
    path('customer/statistics/chart/age/', customer_views.chartAge, name="chart_age"),
    path('setup/', setup_views.pageSetup, name="pageSetup"),
    path('setup/insert/rating/', setup_views.insertRating, name="insert_rating"),
    path('setup/delete/<int:id>/', setup_views.deleteRating, name="delete_rating"),
]