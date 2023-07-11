# Memberships

Manage memberships and membership applications.

Key features:

- Multiple types of membership can be defined with different possible membership statuses. For example, there can be a membership type `Member of Organisation 1` with the status options `active` and `passive` and a membership type `Member of Organisation 2` with the status options `active`, `passive`, and `honorary`.
- Users can apply for a membership through the platform. Each membership type can have its own application form. This form can be customized and combined with other extensions (see [custom registration form](#custom-registration-form)).
- Memberships can require shares that have to be payed once to join the organization, with the possibility to sign additional shares later on. They can also require regular fees that have to be payed periodically. For both cases, automatic invoices are generated if the [payments](payments.md) extension is installed.


## Installation

Add `collectivo.emails` to `extensions` in [`collectivo.yml`](reference.md#settings).

### Custom registration form

The setting `registration_serializers` can be used to add additional pages to the registration form. Entries can be `create` (to create a new object) or `update` (to update an existing object) and must define a path to a [`ModelSerializer`](https://www.django-rest-framework.org/api-guide/serializers/).

In the following example, the registration form will consist of two pages to update the user's [`Profile`](profiles.md) and [`PaymentProfile`](payments.md) and a third page with the default serializer to create a new [`Membership`](#collectivo.memberships.models.Membership).

```yaml title="collectivo.yml"
- extensions:
  - collectivo.memberships:
      - registration_serializers:
          - update: collectivo.profiles.serializers.ProfileRegisterSerializer
          - update: collectivo.payments.serializers.PaymentProfileSerializer
          - create: collectivo.memberships.serializers.MembershipRegisterSerializer
```

[Custom extensions]((../development.md#develop-custom-extensions)) can be used to define additional serializers. The following rules apply:

- Each serializer must have a unique field `user` that will automatically be set to the currently authenticated user. When `update` is used, the model instance to be updated is selected based on the user.

- The schema for [`Membership`](#collectivo.memberships.models.Membership) will be overridden to automatically select the membership type and status options of the current form. E.g. if the user is applying for a membership type with the status options `active` and `passive`, then this type will automatically be selected when submitting the form and the schema for the `status` field will be overridden to only allow `active` and `passive` as values.

## Reference

:::collectivo.memberships.models.Membership
    options:
        members: None

:::collectivo.memberships.models.MembershipType
    options:
        members: None

:::collectivo.memberships.models.MembershipStatus
    options:
        members: None
