# Proyecto final de la materia de Diseño de Aplicaciones Web.
# Intrucciones para ejecutar el proyecto

1.- Clonar el proyecto en tu maquina local.

2.- Crear una base de datos en PostgreSQL con el nombre de "Cliente_Usuario".

3.- Ejecutar pip install -r requirements.txt para instalar las dependencias (tener instalado python antes de hacer esto).

4.- Modificar los settings de la base de datos en el archivo settings.py que se encuentra en la carpeta "Cognitive_Crusaders_Ent".

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Cliente_Usuario',
        'USER': '(Nombre de tu usuario en postgresql)',
        'PASSWORD': '(tucontrasenia)',
        'HOST': 'localhost',
        'PORT': '5432' (puede cambiar OJO)
    }
}

5.- En su consola de comandos, dirigirse a la carpeta del proyecto y ejecutar el comando "py manage.py makemigrations" y después "py manage.py migrate".

6.- En su consola, en la carpeta de su proyecto ejecutar "py manage.py runserver"