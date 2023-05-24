from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomUserCreationFormExtendedTrabajador
from django.contrib.auth import authenticate, login
from .models import Administrador, Cliente, Trabajador
from django.contrib.auth.models import Group, User
from django.utils import timezone

def Inicio(Request):
    return render(Request, 'Inicio.html', {'request': Request})
    # template = loader.get_template("Inicio.html")
    # return HttpResponse(template.render())

@login_required()
def Servicios(Request):
    # template = loader.get_template("servicios.html")
    # return HttpResponse(template.render())
    return render(Request, 'servicios.html', {'request': Request})

def Salir(Request):
    logout(Request)
    template = loader.get_template("Inicio.html")
    return HttpResponse(template.render()) 

def Register(Request):

    data = {
        'form': CustomUserCreationForm()
    }

    if Request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=Request.POST)

        # Agregamos el usuario a la tabla de clientes
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            cliente = Cliente(
                username = user.username,
                nombre=user.first_name,
                apellido=user.last_name,
                correo=user.email,
            )
            cliente.save()

            # Agregamos el usuario al grupo de clientes
            try:
                clientes = Group.objects.get(name='Clientes')
            except Group.DoesNotExist:
                clientes = Group.objects.create(name='Clientes')
            user.groups.add(clientes)

            # Autenticamos y logeamos al usuario
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(Request, user)
            return render(Request, 'Inicio.html', {'request': Request})
    return render(Request, 'registration/register.html', data)

def Login(Request):
    return render(Request, 'registration/login.html', {'request': Request})


@user_passes_test(lambda user: user.is_superuser)
def AgregarTrabajadores(Request):


    if Request.method == 'POST':
        user_creation_form = CustomUserCreationFormExtendedTrabajador(data=Request.POST)
        # Agregamos el usuario a la tabla de clientes
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            administrador = User.objects.get(id=Request.user.id)
            trabajador = Trabajador (
                username = user.username,
                nombre=user.first_name,
                apellido=user.last_name,
                correo=user.email,
                Sueldo=user_creation_form.cleaned_data['sueldo'],
                Fecha_Ingreso=timezone.now(),
                Especialidad=user_creation_form.cleaned_data['especialidad'],
                #fk_Administrador=administrador
            )
            trabajador.save()

            # Agregamos el usuario al grupo de clientes
            try:
                Trabajadores = Group.objects.get(name='Trabajadores')
            except Group.DoesNotExist:
                Trabajadores = Group.objects.create(name='Trabajadores')
            user.groups.add(Trabajadores)

            # Autenticamos y logeamos al usuario
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            #login(Request, user)
            return render(Request, 'Inicio.html', {'request': Request})
    else:
        user_creation_form = CustomUserCreationFormExtendedTrabajador()
        
    data = {
    'form': user_creation_form
    }

    return render(Request, 'registration/AgregarTrabajadores.html', data)


def index(Request):
    return render(Request, 'index.html')