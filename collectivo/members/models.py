"""Models of the members extension."""
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save  # , pre_save, post_delete
from collectivo.utils import get_auth_manager


class Member(models.Model):
    """A member of the collective."""

    # Data from keycloak
    user_id = models.UUIDField(null=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    email_verified = models.BooleanField()

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


# @receiver(pre_save, sender=Member)
# def sync_keycloak_data(sender, instance, **kwargs):
#     """Update changes to the keycloak server."""
#     pass  # _sync_keycloak_data(sender, instance, **kwargs)


# def _sync_keycloak_data(sender, instance, **kwargs):
#     # TODO Check if email == username in this case
#     # TODO Catch errors (or try if already caught)
#     # TODO Write tests
#     # TODO How to confirm new email address?

#     # If object is not connected to auth server
#     if instance.user_id is None:
#         return

#     # If object is just being created
#     if instance.id is None:
#         changes = True
#         new_password = False

#     # Else, check if user data or password has changed
#     else:
#         current = instance
#         previous = Member.objects.get(id=instance.id)
#         changes = any(
#             [getattr(current, field) != getattr(previous, field)
#             for field in ('given_name', 'family_name', 'email')]
#         )
#         new_password = current.password != previous.password

#     # Set up keycloak connection
#     if changes or new_password:
#         keycloak_admin = KeycloakManager().keycloak_admin

#     # Send new user data to keycloak
#     if changes:
#         keycloak_admin.update_user(
#             user_id=instance.user_id,
#             payload={
#                 'firstName': instance.given_name,
#                 'lastName': instance.family_name,
#                 'email': instance.email,
#             }
#         )

#     # Send new password to keycloak
#     if new_password:
#         keycloak_admin.set_user_password(
#             user_id=instance.user_id,
#             password=current.password,
#             temporary=False
#         )


# @receiver(post_save, sender=Member)
# def update_member_groups(sender, instance, created, **kwargs):
#     """Add user to group 'members' if created or updated."""
#     if instance.user_id:
#         get_auth_manager().add_user_to_group(instance.user_id, 'members')

#     # TODO Add user to additional groups
#     # if instance.type == 'active':
#     # set_user_groups(instance.user_id, groups)
