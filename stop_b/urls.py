"""stop_b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import path
import stopBApp.views as views

def custom_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path("logout/", custom_logout, name="logout"),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('bustime/', views.Bustime.as_view(), name='bustime'),
    path('stopnearby/', views.location, name='stopnearby'),
]
