from django.contrib import admin
from .models import Rol, Usuario, Cliente, Administrador, Trabajador, TipoPedido, Estado, Pedido, PedidoTrabajador

admin.site.register(Rol)
#admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Administrador)
admin.site.register(Trabajador)
admin.site.register(TipoPedido)
admin.site.register(Estado)
admin.site.register(Pedido)
admin.site.register(PedidoTrabajador)



