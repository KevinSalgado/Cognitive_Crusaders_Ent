from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('servicios/', views.Servicios, name='Servicios'),
    path('salir/', views.Salir, name='Salir'),
]