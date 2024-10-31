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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password)
        if user:
            #login
            return JsonResponse(
                {'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid username or password'})
    return JsonResponse(
        {'status': 'error', 'message': 'Invalid request method'})

def settings(request):
    return render(request, "web_server/settings.html")
