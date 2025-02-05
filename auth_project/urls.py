"""
URL configuration for auth_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from django.urls import path
from accounts.views import signup_view, login_view, logout_view, verify_email, about_view,home,truncate_users

urlpatterns = [
    path('', home, name='home'),  # Home route added

    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('about/', about_view, name='about'),
    path('truncate-users/', truncate_users, name='truncate_users'),

]

