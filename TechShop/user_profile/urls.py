
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.profile_page, name='profile_page'),
    path('whish/', views.whish_page, name='whish_page'),
    path('orders/',views.orders_page, name='orders_page'),
    path('remove_wish/<int:product_id>/', views.remove_wish, name='remove_wish_page')
]
