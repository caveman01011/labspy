from django.apps import AppConfig


class LabspacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'labspaces'

    def ready(self):
        import labspaces.signals
