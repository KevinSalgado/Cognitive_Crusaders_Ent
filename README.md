# **Proyecto final de la materia de Diseño de Aplicaciones Web.**
# Intrucciones para ejecutar el proyecto

## **Pasos**
1. Clonar el proyecto en tu máquina local. Para ello, a través de su terminal, navegue a la ruta donde quiera descargar el repo y ejecute el siguiente comando:

```
git clone https://github.com/KevinSalgado/Cognitive_Crusaders_Ent.git
```

2. Crear una base de datos en PostgreSQL con el nombre de "Cliente_Usuario".
Para ello, abra su terminal, conéctese a su servidor de PostgreSQL
y ejecute los siguientes comandos:

```
psql -U username

Password for user username: (ingresa tu contraseña)

username=# CREATE DATABASE "Cliente_Usuario";
```

**Nota:** Es importante escribir entre paŕentesis el nombre de la base de datos.


3. Navegue hacia la ruta del proyecto (`cd Cognitive_Crusaders_Ent`) y ejecute `pip install -r requirements.txt` para instalar las dependencias necesarias (tener instalado python antes de hacer esto).

4. Modifique los settings de la base de datos en el archivo [settings.py](Cognitive_Crusaders_Ent/Cognitive_Crusaders_Ent/settings.py) que se encuentra en la carpeta "Cognitive_Crusaders_Ent".

```
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
```

5. En su consola de comandos, diríjase a la carpeta del proyecto principal y ejecute los siguientes comandos:
```
py manage.py makemigrations
py manage.py migrate
```

6. Ejecute en su base de datos los archivos .sql que se encuentran dentro de la carpeta "INSERTS".

7. Ejecute el siguiente comando para crear un superusuario, el cual va a ser necesario para acceder a la página de administración de Django, poder agregar trabajadores, visualizar pedidos, y demás funcionalidades de la aplicación web:
```
py manage.py createsuperuser
```

9. Ejecute los archivos que están en la carpeta "Triggers" en su base de datos, comenzando con el archivo llamado "Function_Copiar_Registro" y después con el archivo llamado "Trigger_copiar_registro".

10. Para ejecutar el proyecto, colóquese en la carpeta principal del proyecto, y ejecute:
```
py manage.py runserver
```