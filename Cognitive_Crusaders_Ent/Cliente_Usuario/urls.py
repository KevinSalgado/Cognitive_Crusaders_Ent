from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'), # views.index
    #path('servicios/', views.Servicios, name='Servicios'),
    path('salir/', views.Salir, name='Salir'),
    path('register/', views.Register, name='Register'),
    path('AgregarTrabajadores/', views.AgregarTrabajadores, name='AgregarTrabajadores'),
    path('login/', views.Login, name='login'),
    path('VisualizarTrabajadores/', views.VisualizarTrabajadores, name='VisualizarTrabajadores'),
    path('Pedido/', views.Pedido, name='Pedido'),
    path('Pedidos_del_Usuario/', views.Pedidos_del_Usuario, name='Pedidos_del_Usuario'),
    path('Pedidos_pendientes/', views.Pedidos_pendientes, name='Pedidos_pendientes'),
    path('Pedidos_empleados/', views.Pedidos_empleados, name='Pedidos_empleados'),
    path('Monitor_Pedidos/', views.Monitor_Pedidos, name='Monitor_Pedidos'),
    path('Prueba_gratuita/', views.Prueba_gratuita, name='Prueba_gratuita'),
    #path('register/', views.Register, name='signup'),
    # path('index/', views.index, name='index')
    path('team/', views.team, name='Team'),
    path("admin/", views.admin, name="admin"),
]