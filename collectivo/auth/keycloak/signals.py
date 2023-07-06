"""Signals of the keycloak extension."""
from django.contrib.auth import get_user_model
from django.db.models import signals

from .models import KeycloakUser


def update_keycloak_user(sender, instance, created, **kwargs):
    """Create or update related keycloak user when a django user is changed."""
    try:
        instance.keycloak.save()
    except KeycloakUser.DoesNotExist:
        KeycloakUser.objects.create(user=instance)


signals.post_save.connect(
    update_keycloak_user,
    sender=get_user_model(),
    dispatch_uid="update_keycloak_user",
    weak=False,
)
