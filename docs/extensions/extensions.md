# Extensions

Manage extensions. This extension is required to register other extensions.

## Installation

Add `collectivo.extensions` to `extensions` in [`collectivo.yml`](../reference.md#settings).

## Usage by other extensions

A [custom extension](../development.md#develop-custom-extensions) can register itself as follows:

```python
from collectivo.extensions.models import Extension

Extension.objects.register(
    name='my_extension',
    description='This is my first custom extension.',
)
```

## Reference

:::collectivo.extensions.models.Extension
    options:
        members: None
