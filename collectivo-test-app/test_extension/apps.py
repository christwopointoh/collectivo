from django.apps import AppConfig


class TestExtensionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_extension'

    collectivo_extension = True
