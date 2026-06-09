from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pagar/', views.comprobante_cuota, name='pagar'),
    path('admin_panel/gestion_comprobantes/', views.gestion_comprobantes, name='gestion_comprobantes'),
]
