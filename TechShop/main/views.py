from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from shop.SupporPrograms.recomendation import no_data_rec
from . import forms
from . import models


def home_page(request):

    if request.user.is_authenticated:

        if request.method == 'GET':
            # last_list = []
            # last_product = []
            last_viewed = models.ViewProduct.objects.filter(user=request.user).order_by('-viewed_at')
            # for i in last_viewed:
            #     if i.product not in last_product:
            #         last_product.append(i.product)
            #         last_list.append(i)
            #         if len(last_list) >= 10:
            #             break
            # last_viewed = last_list

            recomendations = None

            if last_viewed:
                category_viewed_list = []

                for cat in last_viewed:
                    category_viewed_list.append(str(cat.product.category.name))

                print(category_viewed_list) 

                for view in last_viewed:
                    view.image = models.ImageProduct.objects.filter(product=view.product)[0].image


                prod = models.Product.objects.all()
                rec = no_data_rec(prod, 4)

                for p in rec:
                    p.image = models.ImageProduct.objects.filter(product=p)[0].image

                data = {
                    'last_viewed': last_viewed,
                    'recommendations': rec
                }
                return render(request, 'main/home_page.html', data)

            else:
                prod = models.Product.objects.all()
                rec = no_data_rec(prod, 4)

                for p in rec:
                    p.image = models.ImageProduct.objects.filter(product=p)[0].image

                data = {
                    'last_viewed': None,
                    'recommendations': rec
                }
                return render(request, 'main/home_page.html', data)
            
        else:
            return redirect('home_page')
        
    else:
        prod = models.Product.objects.all()
        rec = no_data_rec(prod, 4)

        for p in rec:
            p.image = models.ImageProduct.objects.filter(product=p)[0].image

        data = {
            'last_viewed': None,
            'recommendations': rec
        }
        return render(request, 'main/home_page.html', data)
    

def register_page(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'main/register_page.html', {'form': forms.RegisterForm()})

        elif request.method == 'POST':
            form = forms.RegisterForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                new_user = User(username=username, email=email)
                new_user.set_password(password)
                new_user.save()

                return redirect('home_page')
            else:
                return redirect('register_page')
    else:
        return redirect('home_page')


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'main/login_page.html', {'form': forms.LoginForm()})
        
        elif request.method == 'POST':
            form = forms.LoginForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home_page')
                else:
                    form.add_error(None, "Wrong name or password")

            else:
                return redirect('login_page')

    else:
        return redirect('home_page')
    

def logout_page(request):
    logout(request)
    return redirect('home_page')


def about_page(request):
    data = {
        'workers': models.Worker.objects.all()
    }
    return render(request, 'main/about_page.html', data)

def contact_page(request):
    return render(request, 'main/contact_page.html')