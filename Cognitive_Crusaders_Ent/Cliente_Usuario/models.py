from django.db import models


class Rol(models.Model):
    id_rol = models.BigAutoField(primary_key=True, serialize=True, verbose_name='ID')
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
class Usuario(models.Model):
    id_usuario =  models.BigAutoField( primary_key=True, serialize=True, verbose_name='ID')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    fk_Rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

class Cliente(Usuario):
    Observaciones = models.CharField(max_length=50)

class Administrador(Usuario):
    Sueldo = models.FloatField()

class Trabajador(Usuario):
    Sueldo = models.FloatField()
    fk_Administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

class TipoPedido(models.Model):
    id_tipoPedido = models.BigAutoField(primary_key=True, serialize=True, verbose_name='ID')
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

class Estado(models.Model):
    id_estado = models.BigAutoField(primary_key=True, serialize=True, verbose_name='ID')
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
class Pedido(models.Model):
    id_pedido = models.BigAutoField(primary_key=True, serialize=True, verbose_name='ID')
    Alcance = models.CharField(max_length=50)
    Plazo_inicio = models.DateField()
    Plazo_fin = models.DateField()
    Presupuesto = models.FloatField()
    Info_adicional = models.CharField(max_length=50)
    fk_Estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fk_Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fk_TipoPedido = models.ForeignKey(TipoPedido, on_delete=models.CASCADE)


class PedidoTrabajador(models.Model):
    id_pedidoTrabajador = models.BigAutoField(primary_key=True, serialize=True, verbose_name='ID')
    fk_Pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fk_Trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
