from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
from .models import Caudal
from .models import Clima

def transf (INF_Label : str):
    clima_path = Clima.objects.all().values()
    df_clima = pd.DataFrame.from_dict(clima_path)

    caudales_path = Caudal.objects.all().values()
    dataframe = pd.DataFrame.from_dict(caudales_path)

    #Filtramos por Sector
    dataframe = dataframe.loc[(dataframe["Canonical"]=="CAUDAL") & (dataframe["INF_Label"]==INF_Label)]
    
    #Extraemos la fecha aparte
    dataframe['fecha']=dataframe['RowKey'].dt.date
    #Extraemos la hora aparte
    dataframe['hora']=dataframe['RowKey'].dt.time

    #Convertimos la fecha en formato date
    dataframe['fecha'] = pd.to_datetime(dataframe['fecha'])

    #Hacemos limpieza de los datos del clima que no necesitaremos
    df_clima_clean = df_clima.drop(columns=["visibility","id"])
    #Sacamos la fecha en una columna diferente
    df_clima_clean['fecha']=df_clima_clean['datetimeStr'].dt.date
    #Le ponemos el formato de datetime a la fecha
    df_clima_clean['fecha'] = pd.to_datetime(df_clima_clean['fecha'])
    #Sacamos el promedio por fecha de la temperatura y humedad
    df_clima_agrup = df_clima_clean.groupby(["fecha"]).mean()
    #Quitamos los indixes
    df_clima_agrup.reset_index()

    #Juntamos la fecha de los caudales con la del clima
    dataframe = pd.merge(df_clima_agrup,dataframe, on="fecha")

    #Dividimos la fecha en año, mes, dia, dia_semana
    dataframe['ano'] = dataframe['fecha'].dt.year
    dataframe['mes'] = dataframe['fecha'].dt.month
    dataframe['dia'] = dataframe['fecha'].dt.day
    dataframe['dia_semana'] = dataframe['fecha'].dt.weekday

    #Renombramos las columnas
    dataframe = dataframe.rename(columns = {"INF_Values":"DATOS","fecha":"FECHA", "hora":"HORA", "ano":"AÑO","mes":"MES","dia":"DIA","dia_semana":"DIA_SEMANA"})

    #Sacamos la hora y minuto de la columna hora
    dataframe['HORA_NUMERICA'] = pd.to_datetime(dataframe['HORA'], format='%H:%M:%S').dt.hour
    dataframe['MINUTO_NUMERICO'] = pd.to_datetime(dataframe['HORA'], format='%H:%M:%S').dt.minute


    return dataframe