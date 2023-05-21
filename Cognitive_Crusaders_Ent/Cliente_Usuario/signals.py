from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db.models.signals import post_save

# @receiver(post_save, sender=User)
# def add_user_to_clientes_group(sender, instance, created, **kwargs):
#     if created:
#         try:
#             clientes = Group.objects.get(name='Clientes')
#         except Group.DoesNotExist:
#             clientes = Group.objects.create(name='Clientes')
#         instance.groups.add(clientes)
        #instance.groups.add(Group.objects.get(name='Clientes'))
