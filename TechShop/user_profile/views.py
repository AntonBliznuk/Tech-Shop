from django.shortcuts import render, redirect
from main import models


def profile_page(request):
    if request.user.is_authenticated and request.method == 'GET':
        return render(request, 'user_profile/profile_page.html')
    else:
        return redirect('home_page')




def whish_page(request):
    if request.user.is_authenticated and request.method == 'GET':

        w = models.WhisList.objects.all()

        for i in w:
            prod = i.product
            img = models.ImageProduct.objects.filter(product=prod)[i]
            i.image = img
        
        data = {
            'whish': models.WhisList.objects.all()
        }
        return render(request, 'user_profile/whish_page.html', data)

    else:
        return redirect('home_page')
    



def orders_page(request):
    if request.user.is_authenticated and request.method == 'GET':
        return render(request, 'user_profile/orders_page.html')
    else:
        return redirect('home_page')