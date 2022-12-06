"""Serializers of the members extension."""
from rest_framework import serializers
from . import models

conditions = {
    'sepa': {
        'field': 'shares_payment_type',
        'condition': 'exact',
        'value': 'sepa'
    },
    'natural': {
        'field': 'person_type',
        'condition': 'exact',
        'value': 'natural'
    },
    'legal': {
        'field': 'person_type',
        'condition': 'exact',
        'value': 'legal'
    },
}

field_settings = {
    'id': {
        'permissions': ['read', 'table'],
        'kwargs': {
            'label': 'Membership number',
            'help_text': 'This number can be used to identify you.',
        },
    },
    'email': {
        'permissions': ['read', 'table'],
    },
    'person_type': {
        'permissions': ['create', 'table'],
        'kwargs': {'required': True},
    },
    'first_name': {
        'permissions': ['read', 'create', 'table'],
        'kwargs': {'required': True},
    },
    'last_name': {
        'permissions': ['read', 'create', 'table'],
        'kwargs': {'required': True},
    },
    'gender': {
        'permissions': ['read', 'create', 'change'],
        'kwargs': {'required': True},
    },
    'birthday': {
        'permissions': ['create'],
        'schema': {
            'condition': conditions['natural'],
            'required': True
        }
    },
    'address_street': {
        'permissions': ['read', 'create', 'change'],
        'kwargs': {'required': True},
    },
    'address_number': {
        'permissions': ['read', 'create', 'change'],
        'kwargs': {'required': True},
    },
    'address_stair': {
        'permissions': ['read', 'create', 'change'],
    },
    'address_door': {
        'permissions': ['read', 'create', 'change'],
    },
    'address_postcode': {
        'permissions': ['read', 'create', 'change', 'table'],
        'kwargs': {'required': True},
    },
    'address_city': {
        'permissions': ['read', 'create', 'change'],
        'kwargs': {'required': True},
    },
    'address_country': {
        'permissions': ['read', 'create', 'change', 'table'],
        'kwargs': {'required': True},
    },
    'phone': {
        'permissions': ['read', 'create', 'change'],
    },

    # Legal person fields
    'legal_name': {
        'permissions': ['create'],
        'schema': {
            'condition': conditions['legal'],
            'required': True
        }
    },
    'legal_type': {
        'permissions': ['create'],
        'schema': {
            'condition': conditions['legal'],
            'required': True
        }
    },
    'legal_id': {
        'permissions': ['create'],
        'schema': {
            'condition': conditions['legal'],
            'required': True
        }
    },

    # Membership fields
    'membership_type': {
        'permissions': ['create', 'table'],
        'schema': {
            'condition': conditions['natural'],
            'required': True
        }
    },
    'membership_start': {
        'permissions': ['read', 'table'],
    },
    'shares_number': {
        'permissions': ['read', 'create', 'table'],
        'kwargs': {
            'label': 'Number of shares',
            'help_text': 'The amount of shares that you own.',
            'required': True,
            'min_value': 1
        }
    },
    'shares_payment_type': {
        'permissions': ['create'],
        'kwargs': {'required': True},
    },
    'bank_account_iban': {
        'permissions': ['create'],
        'schema': {
            'condition': conditions['sepa'],
            'required': True
        }
    },
    'bank_account_owner': {
        'permissions': ['create'],
        'schema': {
            'condition': conditions['sepa'],
            'required': True
        }
    },

    # Registration survey fields
    'survey_contact': {
        'permissions': ['create', 'table'],
    },
    'survey_motivation': {
        'permissions': ['create', 'table'],
    },
    'groups_interested': {
        'permissions': ['create', 'table'],
    },
    'skills': {
        'permissions': ['create', 'table'],
    },

    # Table view
    'user_id': {
        'permissions': ['table'],
    },
    'membership_cancelled': {
        'permissions': ['table'],
    },
    'membership_end': {
        'permissions': ['table'],
    },
    'tags': {
        'permissions': ['table'],
    },
}


# Boolean fields that will be converted to tags
register_fields = [
    f for f, s in field_settings.items()
    if 'create' in s['permissions']
]
profile_read_only_fields = [
    f for f, s in field_settings.items()
    if 'read' in s['permissions']
    and 'change' not in s['permissions']
]
profile_fields = [
    f for f, s in field_settings.items()
    if 'change' in s['permissions']
    or 'read' in s['permissions']
]
summary_fields = [
    f for f, s in field_settings.items()
    if 'table' in s['permissions']
]

tag_fields = {
    'statutes_approved': 'Statutes approved',
    'public_use_approved': 'Public use approved',
    'data_use_approved': 'Data use approved',
    'founding_event': 'Founding event'
}


class MemberSerializer(serializers.ModelSerializer):
    """Base serializer for member serializers."""

    schema_attrs = {
        field: settings['schema']
        for field, settings in field_settings.items()
        if 'schema' in settings
    }

    def validate(self, attrs):
        """Adjust membership type based on person type."""
        if attrs.get('person_type') == 'legal':
            attrs['membership_type'] = 'investing'
        return super().validate(attrs)


class MemberRegisterSerializer(MemberSerializer):
    """Serializer for users to register themselves as members."""

    # Tag fields
    statutes_approved = serializers.BooleanField(write_only=True)
    public_use_approved = serializers.BooleanField(write_only=True)
    data_use_approved = serializers.BooleanField(write_only=True)
    founding_event = serializers.BooleanField(write_only=True)

    class Meta:
        """Serializer settings."""

        model = models.Member
        fields = register_fields + [*tag_fields.keys()] + ['id']
        read_only_fields = ('id',)
        extra_kwargs = {
            field: field_settings[field]['kwargs']
            for field in fields
            if field in field_settings
            and 'kwargs' in field_settings[field]
        }

    def validate(self, attrs):
        """Remove tag fields before model creation."""
        # TODO Include checkboxes in validation
        attrs['tags'] = []
        for field, tag_label in tag_fields.items():
            value = attrs[field]
            attrs.pop(field, None)
            if value is True:
                tag_id = models.MemberTag.objects.get(label=tag_label).id
                attrs['tags'].append(tag_id)
        return super().validate(attrs)


class MemberProfileSerializer(MemberSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        model = models.Member
        fields = profile_fields
        read_only_fields = profile_read_only_fields
        extra_kwargs = {
            field: field_settings[field]['kwargs']
            for field in fields
            if 'kwargs' in field_settings[field]
        }


class MemberSummarySerializer(MemberSerializer):
    """Serializer for admins to get member summaries."""

    class Meta:
        """Serializer settings."""

        model = models.Member
        fields = summary_fields


class MemberAdminSerializer(MemberSerializer):
    """Serializer for admins to manage members in detail."""

    class Meta:
        """Serializer settings."""

        model = models.Member
        fields = '__all__'


class MemberTagCreateSerializer(serializers.ModelSerializer):
    """Serializer for new dashboard tiles."""

    class Meta:
        """Serializer settings."""

        model = models.MemberTag
        fields = '__all__'


class MemberTagSerializer(serializers.ModelSerializer):
    """Serializer for member tags."""

    class Meta:
        """Serializer settings."""

        model = models.MemberTag
        fields = '__all__'


class MemberSkillSerializer(serializers.ModelSerializer):
    """Serializer for member skills."""

    class Meta:
        """Serializer settings."""

        model = models.MemberSkill
        fields = '__all__'


class MemberGroupSerializer(serializers.ModelSerializer):
    """Serializer for member groups."""

    class Meta:
        """Serializer settings."""

        model = models.MemberGroup
        fields = '__all__'


class MemberStatusSerializer(serializers.ModelSerializer):
    """Serializer for member status."""

    class Meta:
        """Serializer settings."""

        model = models.MemberStatus
        fields = '__all__'
