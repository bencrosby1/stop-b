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
from django.shortcuts import redirect
from django.urls import path
from stopBApp.views.bus_times_views import get_nearby_stops
from stopBApp.views.detours_view import active_detours
from stopBApp.views.saved_bus_lines_view import saved_bus_lines
from stopBApp.views.saved_bus_lines_view import saved_bus_lines, save_bus_line, unsave_bus_line


import stopBApp.views as views
import stopBApp.views.bus_times_views as bus_times_views

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
    # path('bustime/', views.Bustime.as_view(), name='bustime'),
    path('stopnearby/', views.location, name='stopnearby'),
    path('account/', views.Account.as_view(), name='account'),
    path('delete/', views.DeleteAccount, name='delete_account'),
    path('edit_password/', views.EditPassword, name='edit_password'),
    path('directions/"', views.Directions.as_view(), name='directions'),
    path('bus-times/', bus_times_views.bus_times_page, name='bus-times-page'),
    path('bus-times/<str:stop_id>/', bus_times_views.get_bus_times, name='bus-times'),
    path('get_nearby_stops/', get_nearby_stops, name='get_nearby_stops'),
    ######################################################################
    path('active-detours/', active_detours, name='active_detours'),
    path('saved-bus-lines/', saved_bus_lines, name='saved_bus_lines'),
    path('save-bus-line/<int:bus_line_id>/', save_bus_line, name='save_bus_line'),
    path('unsave-bus-line/<int:bus_line_id>/', unsave_bus_line, name='unsave_bus_line'),
]

