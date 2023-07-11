# Payments

Manage payment methods, invoices, and subscriptions.

At the moment, no payment provider is included in this extension. There is, however, a custom extension that connects invoices to the ERP System [Lotzapp](https://github.com/MILA-Wien/collectivo-mila/tree/main/collectivo/extensions/mila/lotzapp).

## Installation

Add `collectivo.payments` to `extensions` in [`collectivo.yml`](reference.md#settings).

## Reference

:::collectivo.payments.models.PaymentProfile
    options:
        members: None

:::collectivo.payments.models.Invoice
    options:
        members: None

:::collectivo.payments.models.Subscription
    options:
        members: None
