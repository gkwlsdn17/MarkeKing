from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('signup', views.pageSignup, name='pageSignup'),
    path('signup/check', views.signup, name='signup'),
    path('order', views.pageOrder, name='pageOrder'),
    path('order/submit', views.orderSubmit, name='orderSubmit'),
]