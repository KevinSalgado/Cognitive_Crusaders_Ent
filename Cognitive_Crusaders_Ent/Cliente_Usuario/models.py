from django.db import models
from django.contrib.auth.models import Group, Permission


class Rol(models.Model):
    id_rol = models.BigAutoField(primary_key=True, serialize=True, verbose_name="ID")
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150)


class Usuario(models.Model):
    id_usuario = models.BigAutoField(
        primary_key=True, serialize=True, verbose_name="ID"
    )
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50)
    correo = models.CharField(max_length=150)
    contrasena = models.CharField(max_length=150)
    fk_Rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Cliente(Usuario):
    Observaciones = models.CharField(max_length=150)


class Administrador(Usuario):
    Sueldo = models.FloatField()


class Trabajador(Usuario):
    Sueldo = models.FloatField()
    Fecha_Ingreso = models.DateField(null=True)
    Especialidad = models.CharField(max_length=150, null=True)
    fk_Administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)


class TipoPedido(models.Model):
    id_tipoPedido = models.BigAutoField(
        primary_key=True, serialize=True, verbose_name="ID"
    )
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)



class Status(models.Model):
    id_status = models.BigAutoField(primary_key=True, serialize=True, verbose_name="ID")
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

class Pedido(models.Model):
    id_pedido = models.BigAutoField(primary_key=True, serialize=True, verbose_name="ID")
    Alcance = models.CharField(max_length=200)
    Plazo_inicio = models.DateField()
    Plazo_fin = models.DateField()
    Presupuesto = models.FloatField()
    Info_adicional = models.CharField(max_length=50)
    fk_Status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    fk_Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fk_TipoPedido = models.ForeignKey(TipoPedido, on_delete=models.CASCADE)


class PedidoTrabajador(models.Model):
    id_pedidoTrabajador = models.BigAutoField(
        primary_key=True, serialize=True, verbose_name="ID"
    )
    Fecha_Aceptado = models.DateField(null=True)
    fk_Pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fk_Trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

# Creacion de grupos y permisos
# Creacion de los grupos
group_clientes, _ = Group.objects.get_or_create(name='Clientes')
group_trabajadores, _ = Group.objects.get_or_create(name='Trabajadores')
group_administradores, _ = Group.objects.get_or_create(name='Administradores')

# # Creacion de los permisos
# permiso_ver_pedidos_clientes = Permission.objects.get(codename='ver_pedidos_clientes')
# permiso_ver_pedidos_trabajadores = Permission.objects.get(codename='ver_pedidos_trabajadores')

# # Asignacion de permisos a los grupos
# group_clientes.permissions.add(permiso_ver_pedidos_clientes)
# group_trabajadores.permissions.add(permiso_ver_pedidos_trabajadores)