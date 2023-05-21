from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import Cliente
from django.contrib.auth.models import Group

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
    return render(Request, 'AgregarTrabajadores.html', {'request': Request})


