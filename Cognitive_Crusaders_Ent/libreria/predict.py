from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
from .models import Caudal
from .models import Clima
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score
from time import time
import matplotlib.pyplot as plt

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
    dataframe = dataframe.rename(columns = {"INF_Values":"DATOS","fecha":"FECHA", "hora":"HORA", "ano":"ANO","mes":"MES","dia":"DIA","dia_semana":"DIA_SEMANA"})

    #Sacamos la hora y minuto de la columna hora
    dataframe['HORA_NUMERICA'] = pd.to_datetime(dataframe['HORA'], format='%H:%M:%S').dt.hour
    dataframe['MINUTO_NUMERICO'] = pd.to_datetime(dataframe['HORA'], format='%H:%M:%S').dt.minute

    #Eliminamos las columnas que no nos interesa para los datos
    dataframe = dataframe.drop(columns = (["Canonical","RowKey","INF_Label","STA_Label","Sector_Neta","FECHA","HORA","id"]))
    dataframe = dataframe.rename(columns= {"INF_Value":"DATO","temp":"TEMP","humidity":"HUMEDAD"})

    #Eliminamos los datos 0 
    dataframe = dataframe.drop(dataframe[(dataframe['DATO'] == 0)].index)

    return dataframe

def predic(Dataframe):
    X_prueba = Dataframe.copy()
    X_prueba['FECHA'] = X_prueba['ANO'].astype(str) + "-"+X_prueba['MES'].astype(str) +"-"+ X_prueba['DIA'].astype(str) + " " + X_prueba['HORA_NUMERICA'].astype(str) + ":" + X_prueba['MINUTO_NUMERICO'].astype(str)
    X_prueba['FECHA'] = pd.to_datetime(X_prueba['FECHA'])
    Dataframe = X_prueba

    data = Dataframe.set_index('FECHA')
    data = data.sort_index()

    df_cau_agosto = data[(data.index.strftime('%Y-%m').str.startswith('2021-08')) | (data.index.strftime('%Y-%m').str.startswith('2021-09')) | (data.index.strftime('%Y-%m').str.startswith('2021-10')) | (data.index.strftime('%Y-%m').str.startswith('2021-11'))]
    #df_cau_agosto = data.loc[~((data.index.month == 8) & (data.index.day >= 5) & (data.index.day <= 8)), :]
    df_cau_agosto = df_cau_agosto.drop(["ANO","MES","DIA","DIA_SEMANA","HORA_NUMERICA","MINUTO_NUMERICO"], axis=1)
    # Gráficos
    # ==============================================================================
    plt.style.use('fivethirtyeight')
    plt.rcParams['lines.linewidth'] = 1.5

    # Separación datos train-test
    # ==============================================================================
    steps = 1200
    datos_train = df_cau_agosto[:-steps]
    datos_test  = df_cau_agosto[-steps:]

    print(f"Fechas train : {datos_train.index.min()} --- {datos_train.index.max()}  (n={len(datos_train)})")
    print(f"Fechas test  : {datos_test.index.min()} --- {datos_test.index.max()}  (n={len(datos_test)})")
    print(datos_train)
    DiccTrain = datos_test.copy()
    DiccTrain['FECHA'] = DiccTrain.index
    dicc = DiccTrain.to_dict(orient = 'records')
    print(dicc)
    return dicc
   # fig, ax = plt.subplots(figsize=(10, 3))
   # datos_train['DATO'].plot(ax=ax, label='train')
   # datos_test['DATO'].plot(ax=ax, label='test')
   # ax.legend();
    #features = features = ['TEMP',	'HUMEDAD', 'AÑO', 'MES', 'DIA', 'DIA_SEMANA', 'HORA_NUMERICA', 'MINUTO_NUMERICO']
    #X = Dataframe[features]
    #y = Dataframe["DATO"]
    #X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=0)
    #print("Cantidad de datos en el set de entrenamiento: ", X_train.shape[0])
    #print("Cantidad de datos en el set de validación: ", X_test.shape[0])
    #modelo_4 = RandomForestRegressor()
    #num_samples_100 = len(y_train)
    #resultados = {}
    #nombre_modelo = modelo_4.__class__.__name__ 
    #resultados[nombre_modelo] = (pipeline(modelo_4, num_samples_100, X_train, y_train, X_test, y_test))
    #print("Predicción: ", predict(modelo_4, 29.733333, 37.596667, 2022, 6, 13, 0, hora=9, minuto=15)[0])# predecir un día a una hra