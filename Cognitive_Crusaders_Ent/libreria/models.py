from django.db import models

# Create your models here.
class Caudal(models.Model):
    Canonical = models.CharField(verbose_name='Canonical')
    RowKey = models.DateTimeField(verbose_name='RowKey')
    INF_Label = models.CharField(max_length=100,verbose_name='INF_Label')
    INF_Value = models.FloatField(verbose_name='INF_Value')
    STA_Label = models.CharField(max_length=100,verbose_name='STA_Label')
    Sector_Neta = models.CharField(max_length=100,verbose_name='Sector_Neta')

class Clima(models.Model):
    temp = models.FloatField(verbose_name='temp')
    visibility = models.FloatField(verbose_name='visibility')
    datetimeStr = models.DateTimeField(verbose_name='datetimeStr')
    humidity = models.FloatField(verbose_name='humidity')