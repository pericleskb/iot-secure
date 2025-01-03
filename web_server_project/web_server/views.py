from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from collections import defaultdict
import json

from .models import User, SecurityOptions, Measurement
from .sockets.cipher_selection_socket_update import update_cipher


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
        if user:
            #login
            request.session['logged_in'] = True
            return JsonResponse(
                {'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid username or password'})


def logout(request):
    print("LOGOUT")
    request.session['logged_in'] = False
    return HttpResponseRedirect(reverse("web_server:login"))

def settings(request):
    if request.session.get('logged_in'):
        return render(request, "web_server/settings.html")
    else:
        return HttpResponseRedirect(reverse("web_server:login"))

def get_options(request):
    options = SecurityOptions.objects.all().values()
    data = list(options)
    return JsonResponse(data, safe=False)

def get_measurements(request):
    data = defaultdict(list)
    devices = Measurement.objects.values_list('device_name', flat=True).distinct()
    for device_name in devices:
        # get 100 last measurements for each device in db in chronological order
        measurements = Measurement.objects.filter(device_name=device_name).values('value', 'time').order_by('-time')[:100]
        # create json for each device's measurements
        for measurement in measurements:
            try:
                value = float(measurement['value'])
            except:
                continue
            data[device_name].append({
                "value": round(value, 2),
                "time": measurement['time'].strftime("%d-%m-%Y %H:%M:%S")
            })
    return JsonResponse(data, safe=False)
    
def save_preferences(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        
        if not "selected_cipher" in data: 
            return JsonResponse({"error" : "Invalid request body"}, status=400, safe=False)
            
        new_option = SecurityOptions.objects.filter(option_code=data["selected_cipher"]).first()
        
        if new_option is None:
            return JsonResponse({"error" : "Selected cipher not found on the server"}, status=500, safe=False)
            
        instances = SecurityOptions.objects.all()
        for instance in instances:
            print(instance.option_code)
            print(new_option)
            instance.is_selected = instance.option_code == new_option.option_code
            instance.save()

        update_cipher(new_option.option_code)
        return JsonResponse({"message" : "Preference saved"}, status=200, safe=False)
    
    return JsonResponse({"error" : "Invalid request"}, status=400, safe=False)
