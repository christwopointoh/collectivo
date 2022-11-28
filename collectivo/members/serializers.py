"""Serializers of the members extension."""
from rest_framework import serializers
from .models import Member


# Fields for legal entities
legal_fields = ('legal_name', 'legal_type', 'legal_seat', 'legal_type_id')
legal_condition = {
    'field': 'membership_type', 'condition': 'exact', 'value': 'legal'}
legal_schema_attrs = {
    attr: {'condition': legal_condition} for attr in legal_fields}

# Fields for all members
editable_fields = (
    'title_pre', 'title_post', 'first_name', 'last_name',
    'gender', 'date_birth',
    'email', 'email_2', 'phone', 'phone_2',
    'address_street', 'address_number', 'address_is_home', 'address_co',
    'address_stair', 'address_door', 'address_postcode', 'address_city',
    'address_country',
) + legal_fields
registration_fields = (
    'membership_type',
    'shares_number', 'shares_payment_type', 'shares_installment_plan'
)
readonly_fields = (
    'id',
)
summary_fields = (
    'id', 'first_name', 'last_name',
    'membership_type', 'membership_status',
    'shares_payment_status',
)


class MemberSerializer(serializers.ModelSerializer):
    """Base serializer for member serializers."""

    schema_attrs = legal_schema_attrs


class MemberRegisterSerializer(MemberSerializer):
    """Serializer for users to register themselves as members."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = editable_fields + registration_fields + readonly_fields
        read_only_fields = readonly_fields


class MemberProfileSerializer(MemberSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = editable_fields + readonly_fields
        read_only_fields = readonly_fields


class MemberSummarySerializer(MemberSerializer):
    """Serializer for admins to get member summaries."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = summary_fields


class MemberAdminSerializer(MemberSerializer):
    """Serializer for admins to manage members in detail."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = '__all__'
