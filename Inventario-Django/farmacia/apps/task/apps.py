from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' #por cada modelo va a incrementar los ID(default)
    name = 'apps.task'
