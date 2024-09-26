from django.urls import path
from . import views

urlpatterns = [
    path('page/<int:page_number>/', views.shop_page, name='shop_page'),
    path('product/<int:product_id>/', views.product_page, name='product_page')
]