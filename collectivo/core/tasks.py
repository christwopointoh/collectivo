"""Celery tasks for collectivo_app."""

import ping3
from celery import shared_task


@shared_task(name="collectivo_core_ping")
def collectivo_core_ping():
    """Ping Test if the server is up."""
    try:
        ping3.ping("collectivo")
        print("Task ping collectivo successfull")
    except Exception as e:
        print("Task ping collectivo failed with {}".format(e))
        # Todo Send an email to the admins -> should we use the email module?
