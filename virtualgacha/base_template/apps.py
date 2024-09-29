from django.apps import AppConfig


class BaseTemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_template'
