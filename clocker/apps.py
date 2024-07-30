from django.apps import AppConfig


class ClockerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clocker'

    def ready(self):
        from employee import signals
