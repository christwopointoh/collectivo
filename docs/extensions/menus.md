# Menus

Manage menus and menu items.
## Installation

Add `collectivo.menus` to `extensions` in [`collectivo.yml`](reference.md#settings).

## Usage by other extensions

A menu and menu item can be registered by a [custom extension](../development.md#develop-custom-extensions) as follows:

```python
from collectivo.extensions.models import Extension
from collectivo.menus.models import Menu, MenuItem

my_extension = Extension.objects.get(name="my_extension")

Menu.objects.register(name="main", extension=my_extension)

MenuItem.objects.register(
    name="my_menu_item",
    label="My menu item",
    extension=my_extension,
    route="my_extension/my_component",
    icon_name="pi-user",  # See https://primevue.org/icons/
    parent="main",
    order=1,
)
```

The menus `main` and `admin` are registered by the [core](core.md) extension and will be displayed in the sidebar of the frontend application.

## Reference

:::collectivo.menus.models.Menu
    options:
        members: None

:::collectivo.menus.models.MenuItem
    options:
        members: None
