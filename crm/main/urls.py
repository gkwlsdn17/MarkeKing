from django.urls import path
from .views import main_views, customer_views, setup_views, goods_views, sales_views

urlpatterns = [
    path('', main_views.index),

    # 고객 관리
    path('customer/', customer_views.selectCustomer, name="customer_home"),
    path('customer/insert/' , customer_views.insertCustomer, name="customer_insert"),
    path('customer/insert/view/', customer_views.pageInsertCustomer, name="customer_insert_view"),
    path('customer/detail/<str:customer_id>', customer_views.pageCustomerDetail, name="customer_detail"),
    path('customer/update/', customer_views.updateCustomer, name="customer_update"),
    path('customer/delete/<int:cid>', customer_views.deleteCustomer, name="customer_delete"),
    path('customer/search/detail', customer_views.pageCustomerDetailSearch, name="customer_detail_search"),
    path('customer/statistics/', customer_views.pageStatistics, name="page_statistics"),
    path('customer/statistics/chart/age/', customer_views.chartAge, name="chart_age"),
    path('customer/statistics/chart/sex/', customer_views.chartSex, name="chart_sex"),
    path('customer/statistics/chart/signUp/', customer_views.chartSignUp, name="chart_signUp"),

    # 매출 관리
    path('sales/', sales_views.pageSalesMain, name='pageSalesMain'),
    path('sales/list/', sales_views.pageSalesList, name='pageSalesList'),
    path('sales/detail/<str:order_id>', sales_views.pageSalesDetail, name='pageSalesDetail'),
    path('sales/delivery/list/', sales_views.pageDeliveryList, name='pageDeliveryList'),
    path('sales/cancel/<str:order_id>', sales_views.salesCancel, name='salesCancel'),
    path('sales/cancel/list/', sales_views.pageSalesCancelList, name='pageSalesCancelList'),
    path('sales/cancel/detail/<str:order_id>', sales_views.pageSalesCancelDetail, name='pageSalesCancelDetail'),

    # 제품 관리
    path('goods/', goods_views.pageGoodsMain, name="pageGoodsMain"),
    path('goods/insert/view/', goods_views.pageInsertGoods, name="pageInsertGoods"),
    path('goods/insert/', goods_views.insertGoods, name="insert_goods"),
    path('goods/detail/<str:goods_id>', goods_views.goodsDetail, name="goods_detail"),
    path('goods/update/', goods_views.updateGoods, name='update_goods'),
    path('goods/delete/<int:gid>', goods_views.deleteGoods, name='goods_delete'),

    # 설정
    path('setup/', setup_views.pageSetup, name="pageSetup"),
    path('setup/insert/rating/', setup_views.insertRating, name="insert_rating"),
    path('setup/delete/rating/<int:id>/', setup_views.deleteRating, name="delete_rating"),
    path('setup/insert/goods_type/', setup_views.insertGoodsType, name="insert_goodsType"),
    path('setup/delete/goods_type/<int:id>/', setup_views.deleteGoodsType, name="delete_goodsType"),
]