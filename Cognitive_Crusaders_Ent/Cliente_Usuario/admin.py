from django.contrib import admin
from .models import Rol, Cliente, Administrador, Trabajador, TipoPedido, Pedido, PedidoTrabajador, Status 

admin.site.register(Rol)
#admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Administrador)
admin.site.register(Trabajador)
admin.site.register(TipoPedido)
admin.site.register(Status)
admin.site.register(Pedido)
admin.site.register(PedidoTrabajador)



