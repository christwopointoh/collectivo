"""Models of the user experience module."""
from django.db import models


class MicroFrontend(models.Model):
    """A path to a micro-frontend."""

    name = models.CharField(max_length=255, unique=True, primary_key=True)
    extension = models.ForeignKey(
        'extensions.Extension', on_delete=models.CASCADE, null=True)
    path = models.URLField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=[
            ('modules', 'JS remote entry for web components.'),
            ('html', 'Link to a normal html page.')
        ]
    )

    def __str__(self):
        """Return string representation of the model."""
        return f'Micro-Frontend ({self.name})'


class Menu(models.Model):
    """A menu."""

    name = models.CharField(max_length=255, unique=True, primary_key=True)
    extension = models.ForeignKey(
        'extensions.Extension', on_delete=models.CASCADE, null=True)


class MenuItem(models.Model):
    """A menuitem."""

    name = models.CharField(max_length=255, unique=True, primary_key=True)
    extension = models.ForeignKey(
        'extensions.Extension', on_delete=models.CASCADE, null=True)
    menu = models.ForeignKey(
        'ux.Menu', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    action = models.CharField(
        max_length=50,
        default='default',
        choices=[
            ('default', 'default'),  # Render microfrontend in main window
            ('blank', 'blank')  # Render microfrontend in new page
        ]
    )
    microfrontend = models.ForeignKey(
        'ux.MicroFrontend', on_delete=models.CASCADE, null=True)
