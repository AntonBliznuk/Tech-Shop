from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import forms
from . import models


def home_page(request):

    if request.user.is_authenticated:

        if request.method == 'GET':
            last_viewed = models.ViewProduct.objects.filter(user=request.user).order_by('-viewed_at')[:10]
            recomendations = None

            if last_viewed:
                category_viewed_list = []

                for cat in last_viewed:
                    category_viewed_list.append(str(cat.product.category.name))

                print(category_viewed_list) 

                data = {
                    'last_viewed': last_viewed,
                    'recomendations': recomendations
                }
                return render(request, 'main/home_page.html', data)

            else:
                data = {
                    'last_viewed': None,
                    'recomendations': None
                }
                return render(request, 'main/home_page.html', data)
            
        else:
            return redirect('home_page')
        
    else:

        data = {
            'last_viewed': None,
            'recomendations': None
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
                password = form.cleaned_data['password']

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