from django.contrib import admin
from django.urls import path
from .import views 

urlpatterns = [
    path('', views.index),
    path('Overview', views.Overview),
    path('Document', views.Document),
    path('notFound404', views.notFound404),
    path('contacts/<str:firstName>/<str:lastName>/<str:email>/<str:messenger>', views.contacts),
]
