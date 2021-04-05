from django.apps import AppConfig


class GeneralConfig(AppConfig):
    name = 'general'

    def ready(self):
        import general.signals
