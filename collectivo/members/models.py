"""Models of the members extension."""
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from collectivo.auth.manager import add_user_to_group


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
    # groups


@receiver(post_save, sender=Member)
def update_member_groups(sender, instance, created, **kwargs):
    """Add user to group 'members' if created or updated."""
    if instance.user_id:
        add_user_to_group(instance.user_id, 'members')

    # TODO Add user to additional groups
    # if instance.type == 'active':
    # set_user_groups(instance.user_id, groups)


@receiver(post_delete, sender=Member)  # pre_save?
def remove_member_groups(sender, instance, **kwargs):
    """Remove user from group 'members' if deleted."""
    pass
    # TODO
    # remove_user_from_group(instance.user_id, 'members')
