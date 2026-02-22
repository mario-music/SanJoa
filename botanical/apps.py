from django.apps import AppConfig


class BotanicalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'botanical'
    verbose_name = 'Botanical Management'

    def ready(self):
        # Import signals
        import botanical.signals
