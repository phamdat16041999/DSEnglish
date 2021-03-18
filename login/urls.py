from django.contrib import admin
from django.urls import path
from .import views 

urlpatterns = [
    path('', views.login),
    path('/loginFunction', views.loginFunction),
    path('/logout', views.logout),
]
