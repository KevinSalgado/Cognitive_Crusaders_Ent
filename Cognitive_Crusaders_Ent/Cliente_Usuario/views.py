from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomUserCreationFormExtendedTrabajador, CustomUserCreationFormExtendedCliente
from django.contrib.auth import authenticate, login
from .models import Administrador, Cliente, Trabajador, Rol, Pedido as pedidos_, Status, TipoPedido
from django.contrib.auth.models import Group, User
from django.utils import timezone

# ANTIGUO INICIO
# def Inicio(Request):
#     return render(Request, 'Inicio.html', {'request': Request})
#     # template = loader.get_template("Inicio.html")
#     # return HttpResponse(template.render())

#ANTIGUO SERVICIOS
# @login_required()
# def Servicios(Request):
#     # template = loader.get_template("servicios.html")
#     # return HttpResponse(template.render())
#     return render(Request, 'servicios.html', {'request': Request})

def Salir(Request):
    logout(Request)
    template = loader.get_template("index.html")
    return HttpResponse(template.render()) 

def Register(Request):

    data = {
        'form': CustomUserCreationFormExtendedCliente()
    }

    if Request.method == 'POST':
        user_creation_form = CustomUserCreationFormExtendedCliente(data=Request.POST)

        # Agregamos el usuario a la tabla de clientes
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            fkrolid = Rol.objects.get(id_rol=3)
            cliente = Cliente(
                id_usuario = user.id,
                username = user.username,
                nombre=user_creation_form.cleaned_data['first_name'],
                apellido=user_creation_form.cleaned_data['last_name'],
                correo=user_creation_form.cleaned_data['email'],
                telefono = user_creation_form.cleaned_data['telefono'],
                fk_Rol=fkrolid
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
            return render(Request, 'index.html', {'request': Request})
    return render(Request, 'registration/register.html', data)

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            print("Usuario o contraseña incorrectos")
            return render(request, 'registration/login.html', {'request': request})
            
    return render(request, 'registration/login.html', {'request': request})


@user_passes_test(lambda user: user.is_superuser)
def AgregarTrabajadores(Request):


    if Request.method == 'POST':
        user_creation_form = CustomUserCreationFormExtendedTrabajador(data=Request.POST)
        # Agregamos el usuario a la tabla de clientes
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            administrador = Administrador.objects.get(id_usuario=Request.user.id)
            fkrolid = Rol.objects.get(id_rol=2)
            trabajador = Trabajador (
                id_usuario = user.id,
                username = user.username,
                nombre=user_creation_form.cleaned_data['first_name'],
                apellido=user_creation_form.cleaned_data['last_name'],
                correo=user_creation_form.cleaned_data['email'],
                Sueldo=user_creation_form.cleaned_data['sueldo'],
                Fecha_Ingreso=timezone.now(),
                Especialidad=user_creation_form.cleaned_data['especialidad'],
                telefono = user_creation_form.cleaned_data['telefono'],
                fk_Administrador=administrador,
                fk_Rol=fkrolid
            )
            trabajador.save()

            # Agregamos el usuario al grupo de clientes
            try:
                Trabajadores = Group.objects.get(name='Trabajadores')
            except Group.DoesNotExist:
                Trabajadores = Group.objects.create(name='Trabajadores')
            user.groups.add(Trabajadores)

            # Autenticamos al usuario
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            #login(Request, user)
            return render(Request, 'index.html', {'request': Request})
    else:
        user_creation_form = CustomUserCreationFormExtendedTrabajador()
        
    data = {
    'form': user_creation_form
    }

    return render(Request, 'registration/AgregarTrabajadores.html', data)

def index(Request):
    return render(Request, 'index.html', {'request': Request})

@user_passes_test(lambda user: user.is_superuser)
def VisualizarTrabajadores(Request):
    trabajadores = Trabajador.objects.filter(fk_Administrador=Request.user.id)
    print(trabajadores)
    return render(Request, 'VisualizarTrabajadores.html', {'trabajadores': trabajadores})

#@user_passes_test(lambda user: user.is_group('Clientes'))
@user_passes_test(lambda user: user.groups.filter(name='Clientes').exists())
def Pedido(request):
    if request.method == 'POST':
        alcance = request.POST.get('alcance')
        plazo_inicio = request.POST.get('plazo_inicio')
        plazo_fin = request.POST.get('plazo_fin')
        presupuesto = request.POST.get('presupuesto')
        info_adicional = request.POST.get('info_adicional')
        fk_Cliente_id = request.user.id
        fk_TipoPedido_id = request.POST.get('fk_TipoPedido_id')
        #fk_status_id = request.POST.get('fk_status_id')

        # Obtener los objetos de las tablas relacionadas
        cliente = Cliente.objects.get(id_usuario=fk_Cliente_id)
        pedido = TipoPedido.objects.get(id_tipoPedido=fk_TipoPedido_id)
        status = Status.objects.get(id_status=4)
        # Crear un objeto Pedido y guardar los datos
        pedido_objeto_creado = pedidos_(
            Alcance=alcance,
            Plazo_inicio=plazo_inicio,
            Plazo_fin=plazo_fin,
            Presupuesto=presupuesto,
            Info_adicional=info_adicional,
            fk_Cliente=cliente,
            fk_TipoPedido=pedido,
            fk_Status=status
        )
        pedido_objeto_creado.save()

        # Redireccionar al inicio
        return render(request, 'index.html', {'request': request})
    return render(request, 'Pedido.html', {'request': request})

# def sing_up(Request):
#     return render(Request, 'registration/signup.html')