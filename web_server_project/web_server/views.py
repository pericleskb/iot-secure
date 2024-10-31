from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import  login
from django.http import JsonResponse

from .models import User


def home(request):
    if User.objects.exists():
        return HttpResponseRedirect(reverse("web_server:login"))
    else:
        return HttpResponseRedirect(reverse("web_server:register"))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User(username = username, password = password)
        user.save()
        return HttpResponseRedirect(reverse("web_server:settings"))
    else:
        return render(request, "web_server/register.html")

def login(request): 
    return render(request, "web_server/login.html")

def login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password)
        print
        if user:
            #login
            return JsonResponse(
                {'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid username or password'})

def settings(request):
    return render(request, "web_server/settings.html")

def get_options(request):
    # Define your data. This can be dynamic, fetched from a database, etc.
    options = [
        {
            "optionName": "Option 1",
            "optionTitle": "Title for Option 1",
            "optionDescription": "Description for Option 1"
        },
        {
            "optionName": "Option 2",
            "optionTitle": "Title for Option 2",
            "optionDescription": "Description for Option 2"
        },
        {
            "optionName": "Option 3",
            "optionTitle": "Title for Option 3",
            "optionDescription": "Description for Option 3"
        }
    ]
    return JsonResponse(options, safe=False)
