from django.urls import path

from . import views

app_name = "web_server"
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('login-ajax/', views.login_ajax, name="login_ajax"),
    path('settings/', views.settings, name="settings"),
    path('api/options/', views.get_options, name='get_options'),
]
