from django.urls import path
from . import views

urlpatterns = [
    path('page/<int:page_number>/', views.shop_page, name='shop_page'),
    path('product/<int:product_id>/', views.product_page, name='product_page'),
    path('order/product/<int:product_id>/', views.order_page, name='make_order')
]