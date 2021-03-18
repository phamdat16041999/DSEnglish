from django.contrib import admin
from django.urls import path
from .import views 

urlpatterns = [
    path('', views.createAccount),
    path('/checkDuplicateAccount', views.checkDuplicateAccount),
    path('/insertAccount', views.insertAccount),
    path('/authenticEmail/<int:id>/', views.authenticEmail),
]
