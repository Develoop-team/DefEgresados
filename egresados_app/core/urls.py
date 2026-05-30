from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from core import views

urlpatterns = [
    path('', views.home, name='home'),
]
