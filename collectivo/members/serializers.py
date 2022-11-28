"""Serializers of the members extension."""
from rest_framework import serializers
from .models import Member, MemberTag


# Fields for all members
editable_fields = (
    'gender',
    'phone', 'email',
    'address_street', 'address_number',
    'address_stair', 'address_door', 'address_postcode',
    'address_city', 'address_country',
)

legal_fields = ('legal_name', 'legal_type', 'legal_id')
natural_fields = ('birthday', )
sepa_fields = ('bank_account_iban', 'bank_account_owner')

optional_fields = (
    'address_stair', 'address_door', 'phone',
) + legal_fields + natural_fields + sepa_fields

registration_fields = (
    'first_name', 'last_name', 'person_type',
    'shares_number', 'shares_payment_type',
    'survey_first_heard',
    'survey_motivation',
    'survey_working_groups',
    'survey_skills',
) + legal_fields + natural_fields + sepa_fields

readonly_fields = ('id', 'membership_start',) + registration_fields

summary_fields = (
    'id',
    'first_name', 'last_name',
    'person_type', 'membership_status',
    'membership_start',
    'membership_cancelled',
    'membership_end',
    'tags',
)
tag_fields = (
    # 'statutes_approved', TODO Add nach Gründung
    'public_use_approved',
    'data_use_approved'
)

# Create conditions
schema_attrs = {}


def add_conditions(fields, condition_field, value):
    """Add conditions to schema attributes."""
    condition = {
        'field': condition_field, 'condition': 'exact', 'value': value}
    schema_attrs.update({
        attr: {'condition': condition} for attr in fields})


add_conditions(legal_fields, 'person_type', 'legal')
add_conditions(natural_fields, 'person_type', 'natural')
add_conditions(sepa_fields, 'shares_payment_type', 'sepa')


class MemberSerializer(serializers.ModelSerializer):
    """Base serializer for member serializers."""

    schema_attrs = schema_attrs


class MemberRegisterSerializer(MemberSerializer):
    """Serializer for users to register themselves as members."""

    # Tag fields
    # TODO Add after Gründung
    # statutes_approved = serializers.BooleanField(write_only=True)
    public_use_approved = serializers.BooleanField(write_only=True)
    data_use_approved = serializers.BooleanField(write_only=True)

    class Meta:
        """Serializer settings."""

        model = Member
        fields = editable_fields + registration_fields + tag_fields + ('id',)
        read_only_fields = ('id',)
        extra_kwargs = {
            field: {'required': field not in optional_fields}
            for field in fields
        }
        extra_kwargs['shares_number']['min_value'] = 1

    def validate(self, attrs):
        """Remove tag fields before model creation."""
        # TODO Include checkboxes in validation
        attrs['tags'] = []
        for field in tag_fields:
            value = attrs[field]
            attrs.pop(field, None)
            if value is True:
                attrs['tags'].append(field)
        return super().validate(attrs)


class MemberProfileSerializer(MemberSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = registration_fields + editable_fields + readonly_fields
        read_only_fields = registration_fields + readonly_fields


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


class MemberTagCreateSerializer(serializers.ModelSerializer):
    """Serializer for new dashboard tiles."""

    class Meta:
        """Serializer settings."""

        model = MemberTag
        fields = '__all__'


class MemberTagSerializer(serializers.ModelSerializer):
    """Serializer for existing dashboard tiles."""

    class Meta:
        """
        Serializer settings.

        The name cannot be changed because it is the primary key to identify
        the object. A new object has to be created to set a new name.
        """

        model = MemberTag
        fields = '__all__'
        read_only_fields = ('tag_id', )
