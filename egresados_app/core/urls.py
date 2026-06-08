from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enviar-solicitud/', views.enviar_solicitud, name='enviar_solicitud'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
