from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_default = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):
        import cart.signals