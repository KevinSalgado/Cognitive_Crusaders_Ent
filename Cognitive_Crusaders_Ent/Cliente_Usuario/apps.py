from django.apps import AppConfig


class ClienteUsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cliente_Usuario'
    verbose_name = 'Cliente_Usuario'

    def ready(self):
        import Cliente_Usuario.signals
