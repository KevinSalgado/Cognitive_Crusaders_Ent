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
from skforecast.ForecasterAutoreg import ForecasterAutoreg

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

    # Separación datos train-test
    # ==============================================================================
    steps = 1200
    datos_train = df_cau_agosto[:-steps]
    datos_test  = df_cau_agosto[-steps:]

    print(f"Fechas train : {datos_train.index.min()} --- {datos_train.index.max()}  (n={len(datos_train)})")
    print(f"Fechas test  : {datos_test.index.min()} --- {datos_test.index.max()}  (n={len(datos_test)})")

    # Crear y entrenar forecaster
    # ==============================================================================
    forecaster = ForecasterAutoreg(
                    regressor = RandomForestRegressor(random_state=123,max_depth=10, n_estimators=100),
                    lags = 576
                )
    y=datos_train['DATO']
    forecaster.fit(y)
    print("Listo")
    # Predicciones
    # ==============================================================================
    steps = 1200
    predicciones = forecaster.predict(steps=steps)
    print(predicciones.head(5))

    predicciones.index = pd.Index(datos_test.index)
    print(predicciones.head())

    #DiccTrain = datos_test.copy()
    #DiccTrain['FECHA'] = DiccTrain.index
    #dicc = DiccTrain.to_dict(orient = 'records')
    #print(dicc)
    #return dicc
   

class PredictWaterConsume(object):
    def __init__(self, sector):
        self.df_sector = pd.DataFrame(transf(sector,))
        self.create_date()
        #df_sector.head()


    def create_date(self):
        X_prueba = self.df_sector.copy()
        X_prueba['FECHA'] = X_prueba['AÑO'].astype(str) + "-"+X_prueba['MES'].astype(str) +"-"+ X_prueba['DIA'].astype(str) + " " + X_prueba['HORA_NUMERICA'].astype(str) + ":" + X_prueba['MINUTO_NUMERICO'].astype(str)
        X_prueba['FECHA'] = pd.to_datetime(X_prueba['FECHA'])
        df_sector_temphum = X_prueba
        #df_sector_temphum.head()

        data = df_sector_temphum.set_index('FECHA')
        self.data = data.sort_index()
        #data
        #self.data = data.asfreq('MS')

        
    ### CHECAR ESA FUNCIÓN PORQUE DE AQUÍ DEPENDE LA SEPARACIÓN DE TEST, TRAIN ###
    #def subset_mes(self, year, month):
        # Subset de datos (mes)
    #    self.subset = self.data[(self.data.index.strftime('%Y-%m').str.startswith('{}-{}'.format(year, month)))]
        #df_cau_agosto
    #    self.subset = self.subset.drop(["AÑO","MES","DIA","DIA_SEMANA","HORA_NUMERICA","MINUTO_NUMERICO"], axis=1)

    def split_data(self, steps=900):
        self.datos_train = self.data[:-steps].drop(["AÑO","MES","DIA","DIA_SEMANA","HORA_NUMERICA","MINUTO_NUMERICO"], axis=1)
        self.datos_test  = self.data[-steps:].drop(["AÑO","MES","DIA","DIA_SEMANA","HORA_NUMERICA","MINUTO_NUMERICO"], axis=1)        
    
    def train(self, steps=900, _lags_=144):
        # Separación datos train-test
        # ==============================================================================
        #steps = 900
        ##self.datos_train = self.data[:-steps]
        ##self.datos_test  = self.data[-steps:]

        print(f"Fechas train : {self.datos_train.index.min()} --- {self.datos_train.index.max()}  (n={len(self.datos_train)})")
        print(f"Fechas test  : {self.datos_test.index.min()} --- {self.datos_test.index.max()}  (n={len(self.datos_test)})")

        fig, ax = plt.subplots(figsize=(7, 3))
        self.datos_train['DATO'].plot(ax=ax, label='train')
        self.datos_test['DATO'].plot(ax=ax, label='test')
        ax.legend();

        # Crear y entrenar forecaster
        # ==============================================================================
        self.forecaster = ForecasterAutoreg(
                        regressor = RandomForestRegressor(),
                        lags = _lags_ # 144
                    )
        y = self.datos_train['DATO']
        self.forecaster.fit(y)
        #forecaster


    def predict(self, steps=900):
        # Predicciones
        # ==============================================================================
        #steps = 900
        predicciones = self.forecaster.predict(steps=steps)
        predicciones.head(5)

        
        sub = self.datos_test['DATO'][:steps] ################################################
        predicciones.index = pd.Index(sub.index) ######################################

        predicciones.head()


        # Gráfico Predicciones
        # ==============================================================================
        fig, ax = plt.subplots(figsize=(15, 8))
        self.datos_train['DATO'][-steps:].plot(ax=ax, label='train')
        sub.plot(ax=ax, label='test')
        predicciones.plot(ax=ax, label='predicciones')
        ax.legend();

        return predicciones
 
    def get_error():
        # Error test
        # ==============================================================================
        error_mse = mean_squared_error(
                        y_true = datos_test['DATO'],
                        y_pred = predicciones
                    )

        print(f"Error de test (mse): {error_mse}")

        error_r2_score = r2_score(
                        y_true = datos_test['DATO'],
                        y_pred = predicciones
        )
        print(f"r2_score: {error_r2_score}")