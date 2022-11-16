"""Serializers of the members extension."""
from rest_framework import serializers
from .models import Member
# from drf_spectacular.utils import extend_schema_field

# Write access for users
user_write_attrs = (
    'title_pre', 'title_post', 'first_name', 'last_name',
    'gender', 'date_birth',
    'email', 'email_2', 'phone', 'phone_2',
    'address_street', 'address_number', 'address_is_home', 'address_co',
    'address_stair', 'address_door', 'address_postcode', 'address_city',
    'address_country',

    # Only for legal person
    'legal_name', 'legal_type', 'legal_seat', 'legal_type_id'
)

user_read_attrs = (
    'id',
)

# Write access for create view or admins
user_write_attrs_create = (
    'membership_type',
    'shares_number', 'shares_payment_type', 'shares_installment_plan'
)

# Include in admin list view
admin_list_attrs = (
    'id', 'first_name', 'last_name', 'membership_type', 'membership_status',
)


class MemberCreateSerializer(serializers.ModelSerializer):
    """Serializer for members to create themselves."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = user_write_attrs + user_write_attrs_create + user_read_attrs
        read_only_fields = user_read_attrs


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = user_write_attrs + user_read_attrs
        read_only_fields = user_read_attrs


class MemberAdminSerializer(serializers.ModelSerializer):
    """Serializer for admins to manage members."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = admin_list_attrs


class MemberAdminDetailSerializer(serializers.ModelSerializer):
    """Serializer for admins to manage members in detail."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = '__all__'
