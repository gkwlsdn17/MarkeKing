from django.urls import path
from .views import main_views, customer_views

urlpatterns = [
    path('', main_views.index),
    path('customer/', customer_views.selectCustomer)
]