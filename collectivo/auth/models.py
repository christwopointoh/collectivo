"""Models of the authentication module."""
from django.db import models
from collectivo.auth.services import AuthService


class User(models.Model):
    """A user that corresponds to a user of the authentication service."""

    user_id = models.UUIDField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    roles = models.ManyToManyField("Role", blank=True)
    events = models.ManyToManyField("Event", blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        """Return string representation."""
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        """Save model. Get or create auth user if a new instance is created."""
        if not self.pk:
            self.user_id = self.get_or_create_auth_user()
        super().save(*args, **kwargs)

    def get_or_create_auth_user(self):
        """Return existing user id or create new auth user."""
        auth = AuthService()
        user_id = auth.get_user_id(self.email)
        if user_id is None:
            user_id = auth.create_user(
                self.first_name, self.last_name, self.email
            )
        return user_id


class Role(models.Model):
    """A role that can be assigned to users
    (synced with auth service)."""

    label = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """Return string representation."""
        return f"Role ({self.label})"


class Event(models.Model):
    """An event that can be assigned to users
    (not synced with auth service)."""

    label = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """Return string representation."""
        return f"Event ({self.label})"
