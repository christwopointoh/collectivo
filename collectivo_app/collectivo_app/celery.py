"""Celery configuration module."""
import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collectivo_app.settings")

app = Celery("collectivo_app")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Import schedules from installed apps
extension_schedules = {}
for app_name in settings.INSTALLED_APPS:
    try:
        import importlib

        app_module = importlib.import_module(app_name + ".schedules")
        if hasattr(app_module, "schedules") and isinstance(
            app_module.schedules, dict
        ):
            extension_schedules.update(app_module.schedules)
    except ModuleNotFoundError:
        pass

# Set up periodic tasks
app.conf.beat_schedule = {
    **extension_schedules,
}
