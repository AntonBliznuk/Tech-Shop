from django.shortcuts import render, HttpResponse
from django.views.generic import View


class HomePage(View):
    def get(self, request):
        return HttpResponse("Home Page")