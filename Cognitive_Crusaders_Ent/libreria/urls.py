from django.urls import path
from . import views

app_name = 'libreria'

urlpatterns = [
    path('',views.index, name='graph_index'),
    path('get_chart', views.get_chart, name = 'get_chart'),
]