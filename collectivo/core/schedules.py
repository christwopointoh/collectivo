"""Celery schedules of the core module."""
from celery.schedules import crontab

schedules = {
    # Execute the Ping Test every 1 minutes
    "collectivo_core_ping_1min": {
        "task": "collectivo_core_ping",
        "schedule": crontab(minute="*/1"),
    },
}
