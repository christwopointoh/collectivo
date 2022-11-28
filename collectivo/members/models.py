"""Models of the members extension."""
from django.db import models


class MemberTag(models.Model):
    """A tag that can be assigned to members."""

    name = models.CharField(max_length=255)
    built_in = models.BooleanField(default=False)


class MemberCard(models.Model):
    """A membership card that can be assigned to members."""

    date_created = models.DateField()
    active = models.BooleanField(default=False)


class MemberAddon(models.Model):
    """A person that can be assigned to members."""

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    person_type = models.CharField(
        max_length=20,
        choices=[
            ('child', 'child'),
            ('coshopper', 'coshopper'),
        ]
    )
    birth_date = models.DateField(null=True)
    membership_card = models.ForeignKey(
        'MemberCard', null=True, on_delete=models.SET_NULL)


class Member(models.Model):
    """A member of the collective."""

    # Account
    user_id = models.UUIDField(null=True, unique=True)
    email = models.EmailField()
    email_verified = models.BooleanField(null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    # Personal data
    person_type = models.CharField(
        help_text='Type of person.',
        max_length=20,
        default='natural',
        choices=[
            ('natural', 'natural'),
            ('legal', 'legal'),
        ]
    )
    gender = models.CharField(
        max_length=20,
        default='diverse',
        choices=[
            ('diverse', 'diverse'),
            ('female', 'female'),
            ('male', 'male'),
        ]
    )
    address_street = models.CharField(max_length=255, null=True)
    address_number = models.CharField(max_length=255, null=True)
    address_stair = models.CharField(max_length=255, null=True)
    address_door = models.CharField(max_length=255, null=True)
    address_postcode = models.CharField(max_length=255, null=True)
    address_city = models.CharField(max_length=255, null=True)
    address_country = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)

    # FUTURE Personal data (only for active members)
    # FUTURE kids = models.ManyToManyField('MemberAddon')
    # FUTURE coshoppers = models.ManyToManyField('MemberAddon')

    # Personal data (only for natural people)
    birthday = models.DateField(null=True)

    # Personal data (only for legal person)
    legal_name = models.CharField(max_length=255, null=True)
    legal_type = models.CharField(max_length=255, null=True)
    legal_id = models.CharField(max_length=255, null=True)

    # Membership
    membership_start = models.DateField(null=True)
    membership_cancelled = models.DateField(null=True)
    membership_end = models.DateField(null=True)
    membership_status = models.CharField(
        max_length=20,
        help_text='Current status of membership.',
        default='1_applicant',
        choices=[
            ('applicant', 'applicant'),
            ('provisional', 'provisional'),
            ('active', 'active'),
            ('investing', 'investing'),
            ('ended', 'ended'),
        ]
    )
    membership_card = models.ForeignKey(
        'MemberCard', null=True, on_delete=models.SET_NULL)

    # Membership - Coop shares
    shares_number = models.IntegerField(null=True)
    shares_payment_date = models.DateField(null=True)
    shares_payment_type = models.CharField(
        max_length=20,
        help_text='Type of payment.',
        null=True,
        choices=[
            ('sepa', 'sepa'),
            ('transfer', 'transfer')
        ]
    )
    bank_account_iban = models.CharField(max_length=255, null=True)
    bank_account_owner = models.CharField(max_length=255, null=True)
    # FUTURE shares_installment_plan = models.BooleanField(default=False)

    # Survey data
    survey_first_heard = models.TextField(null=True)
    survey_motivation = models.TextField(null=True)
    survey_working_groups = models.TextField(null=True)
    survey_skills = models.TextField(null=True)

    # Other
    tags = models.ManyToManyField('MemberTag')
    admin_notes = models.TextField(null=True)
