from django.apps import AppConfig

class EproConfig(AppConfig):
    name = "epro"

    def ready(self):
        from . import signals

