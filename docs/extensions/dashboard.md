# Dashboard

Create a starting page for your plattform with a dashboard that can display custom tiles.

## Installation

Add `collectivo.dashboard` to `extensions` in [`collectivo.yml`](../reference.md#settings).

## Usage by other extensions

A dashboard tile and tile button can be registered by a [custom extension](../development.md#develop-custom-extensions) as follows:

```python
from collectivo.extensions.models import Extension
from collectivo.dashboard.models import DashboardTile, DashboardTileButton

my_extension = Extension.objects.get(name="my_extension")

tile = DashboardTile.objects.register(
    name="my_extension_welcome_tile",
    label="My extension tile",
    extension=my_extension,
    source="db",
    order=0,
    content=(
        "Welcome {{ user.first_name }} {{ user.last_name }}. "
        "This tile has been created by my_extension."
    ),
)

button = DashboardTileButton.objects.register(
    name=f"example_button_{i}",
    label=f"Example Button {i}",
)

tile.buttons.set([button])
```

## Reference

:::collectivo.dashboard.models.DashboardTile
    options:
        members: None

:::collectivo.dashboard.models.DashboardTileButton
    options:
        members: None
