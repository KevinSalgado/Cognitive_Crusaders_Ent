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
    dicc = datos_train.to_dict()
    #print(dicc)
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


def predict(modelo, temp, humedad, año, mes, dia, dia_semana, hora=None, minuto=None):
    """
    INPUTS:
    - modelo = modelo entrenado con el que se desea predecir
    - dia 
    - mes
    - año
    - hora
    - minuto
    """
    #modelo = modelo.fit(X_train, y_train)

    # En caso de tener que completar horas y minutos o solo minutos
    hrs = list(range(0, 24))
    mins = list(range(0, 46, 15))

    if hora == None and minuto == None: # DIA MES AÑO
        # completar las 24hrs 15minutales
        hrs_mins = list(itertools.product(hrs, mins))
        df_hrs_mins = pd.DataFrame(hrs_mins, columns=['HORA', 'MINUTO'])
        
        X_pred = [[[temp, humedad, año, mes, dia, dia_semana, hora, minuto]] for hora, minuto in hrs_mins]
        X_pred = np.array(X_pred)
        X_pred = X_pred.reshape(X_pred.shape[0], -1)
        

    elif hora != None and minuto == None: # DIA MES AÑO HORA
        # completar los 15minutales
        hr_mins = list(itertools.product([hora], mins)) # para el producto hora debe ser lista
        df_hr_mins = pd.DataFrame(hr_mins, columns=['HORA', 'MINUTO'])
        
        X_pred = [[[temp, humedad, año, mes, dia, dia_semana, hora, minuto]] for hora, minuto in hr_mins]
        X_pred = np.array(X_pred)
        X_pred = X_pred.reshape(X_pred.shape[0], -1)


    else: # DIA MES AÑO HORA MINUTO
        X_pred = [[temp, humedad, año, mes, dia, dia_semana, hora, minuto]] # predecir


    # predict
    pred = modelo.predict(X_pred)

    return pred    


def pipeline(modelo, sample_size, X_train, y_train, X_test, y_test):
    """
    INPUTS:
        + modelo: modelo ML a utilizar
        + sample_size: tamaño de la muestra que se extraerá del conjunto de training
        + X_train: set de características para training
        + y_train: set de targets para training
        + X_test: set de caracteristicas para testing
        + y_test: set de targets para testing
    """

    resultados = {}

    # El tiempo nos va a servir para medir cuánto tarda el modelo en predecir, esto nos serviría también para elegir un modelo que no demore tanto  
    start = time() # Get start time
    modelo = modelo.fit(X_train[:], y_train[:])
    #modelo = modelo.fit(X_train[:sample_size], y_train[:sample_size])
    end = time() # Get end time

    resultados['tiempo_training'] = end - start
        
    # Obtenemos predicciones del set de validación e igual de los primeros 300 datos del set de entrenamiento para obtener su precisión
    start = time() # Get start time
    predictions_test = modelo.predict(X_test)
    predictions_train = modelo.predict(X_train[:300])
    end = time() # Get end time

    resultados['tiempo_total_pred'] = end - start
            
    resultados['MSE_train'] = mean_squared_error(y_train[:300], predictions_train)
    resultados['MSE_test'] = mean_squared_error(y_test, predictions_test)

    resultados['R2_train'] = r2_score(y_train[:300], predictions_train)
    resultados['R2_test'] = r2_score(y_test, predictions_test)
    
    print("{} entrenado en {} datos.".format(modelo.__class__.__name__, sample_size))
        
    # Return the results
    return resultados    