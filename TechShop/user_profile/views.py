from django.shortcuts import render, redirect
from main import models
from .models import Order


def profile_page(request):
    if request.user.is_authenticated and request.method == 'GET':
        return render(request, 'user_profile/profile_page.html')
    else:
        return redirect('home_page')




def whish_page(request):
    if request.user.is_authenticated and request.method == 'GET':

        w = models.WhisList.objects.filter(user=request.user)

        for i in w:
            prod = i.product
            img = models.ImageProduct.objects.filter(product=prod)[0].image
            i.image = img
        
        data = {
            'whish': w
        }
        return render(request, 'user_profile/whish_page.html', data)

    else:
        return redirect('home_page')
    



def orders_page(request):
    if request.user.is_authenticated and request.method == 'GET':

        w = Order.objects.filter(user=request.user)

        for i in w:
            prod = i.product
            img = models.ImageProduct.objects.filter(product=prod)[0].image
            i.image = img
        
        data = {
            'orders': w
        }
        return render(request, 'user_profile/orders_page.html', data)
    else:
        return redirect('home_page')


def remove_wish(request, product_id):
    if request.user.is_authenticated and request.method == 'GET':
        product = models.Product.objects.get(id=product_id)
        wish = models.WhisList.objects.get(product=product, user=request.user)
        wish.delete()
        return redirect('whish_page')
    else:
        return redirect('whish_page')
