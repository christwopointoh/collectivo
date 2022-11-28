"""Serializers of the members extension."""
from rest_framework import serializers
from .models import Member, MemberTag


# Fields for legal entities
legal_fields = ('legal_name', 'legal_type', 'legal_id')
legal_condition = {
    'field': 'person_type', 'condition': 'exact', 'value': 'legal'}
legal_schema_attrs = {
    attr: {'condition': legal_condition} for attr in legal_fields}

# Fields for all members
editable_fields = (
    'first_name', 'last_name',
    'gender', 'birth_date',
    'email', 'phone',
    'address_street', 'address_number',
    'address_stair', 'address_door', 'address_postcode',
    'address_city', 'address_country',
) + legal_fields
registration_fields = (
    'person_type',
    'shares_number', 'shares_payment_type',
)
readonly_fields = (
    'id',
)
summary_fields = (
    'id', 'first_name', 'last_name',
    'person_type', 'membership_status',
    'tags',
)
tag_fields = (
    'statutes_approved', 'public_use_approved', 'data_use_approved'
)


class MemberSerializer(serializers.ModelSerializer):
    """Base serializer for member serializers."""

    schema_attrs = legal_schema_attrs


class MemberRegisterSerializer(MemberSerializer):
    """Serializer for users to register themselves as members."""

    # Tag fields
    statutes_approved = serializers.BooleanField(
        default=False, write_only=True)
    public_use_approved = serializers.BooleanField(
        default=False, write_only=True)
    data_use_approved = serializers.BooleanField(
        default=False, write_only=True)

    class Meta:
        """Serializer settings."""

        model = Member
        fields = editable_fields + registration_fields + readonly_fields \
            + tag_fields
        read_only_fields = readonly_fields

    def validate(self, attrs):
        """Remove tag fields before model creation."""
        # TODO Logic for tag fields
        for field in tag_fields:
            attrs.pop(field, None)
        return super().validate(attrs)


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

    tags = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=MemberTag.objects.all())

    class Meta:
        """Serializer settings."""

        model = Member
        fields = '__all__'
        # extra_kwargs = {'tags': {'required': False}}
