from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'), # views.index
    path('servicios/', views.Servicios, name='Servicios'),
    path('salir/', views.Salir, name='Salir'),
    path('register/', views.Register, name='Register'),
    path('AgregarTrabajadores/', views.AgregarTrabajadores, name='AgregarTrabajadores'),
    path('login/', views.Login, name='login'),
    # path('index/', views.index, name='index')
]