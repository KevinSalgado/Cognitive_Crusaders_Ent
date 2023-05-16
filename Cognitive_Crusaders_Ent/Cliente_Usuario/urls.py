from django.urls import path
from . import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('servicios/', views.Servicios, name='Servicios'),
]