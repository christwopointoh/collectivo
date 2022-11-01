"""Models of the members extension."""
from django.db import models


class Member(models.Model):
    """A member of the collective."""

    user_id = models.UUIDField(null=True, unique=True)
    user_attr = models.CharField(max_length=255)
    create_attr = models.CharField(max_length=255)
    admin_attr = models.CharField(
        max_length=255, default='default value')

    # Future fields
    # children = models.ManyToManyField('children')
    # coshoppers = models.ManyToManyField('coshoppers')
    # capital = models.IntegerField()
    # capital_status = models.CharField()
    # date_entered
    # date_left
