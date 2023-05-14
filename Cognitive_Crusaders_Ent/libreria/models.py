from django.db import models

# Create your models here.
class Caudal(models.Model):
    Canonical = models.CharField(verbose_name='Canonical')
    #Prubea para cambiar el RowKey a tipo Date para asi poder filtrar las fechas
    #Codigo antes de la prueba:
    #RowKey = models.CharField(verbose_name='RowKey')
    RowKey = models.DateTimeField(verbose_name='RowKey')
    INF_Label = models.CharField(max_length=100,verbose_name='INF_Label')
    INF_Value = models.FloatField(verbose_name='INF_Value')
    STA_Label = models.CharField(max_length=100,verbose_name='STA_Label')
    Sector_Neta = models.CharField(max_length=100,verbose_name='Sector_Neta')