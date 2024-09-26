from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from . import forms


class HomePage(View):
    def get(self, request):
        return HttpResponse("Home Page")
    

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