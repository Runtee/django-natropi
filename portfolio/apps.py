from django.apps import AppConfig


class PortfoiloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'

    def ready(self):
        from .scheduler import start_scheduler_thread
        start_scheduler_thread()
