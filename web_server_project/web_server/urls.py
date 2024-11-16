from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "web_server"
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login_view"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout_view'),
    path('login-ajax/', views.login_ajax, name="login_ajax"),
    path('settings/', views.settings, name="settings"),
    path('api/options/', views.get_options, name='get_options'),
    path('api/measurements/', views.get_measurements, name='get_measurements'),
    path('api/save-preferences/', views.save_preferences, name='save_preferences'),
]
