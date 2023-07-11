# Components

Define external components that can be used in the frontend. An alternative is to add Vue components directly to the frontend code through a [custom extension](../development.md#develop-custom-extensions).

## Installation

Add `collectivo.components` to `extensions` in [`collectivo.yml`](reference.md#settings).

## Usage by other extensions

### Register a component

A component can be registered by a [custom extension](../development.md#develop-custom-extensions) as follows:

```python
from collectivo.extensions.modles import Extension
from collectivo.components.models import Component

Component.objects.register(
    name='my-component',
    type='iframe',
    path='https://example.com',
    extension=Extension.objects.get(name='my-extension'),
)
```

There are two types of components:

- `iframe`: The component is displayed as an iframe.
- `remote`: The component is displayed as a remote webcomponent, using [vite-plugin-federation](https://github.com/originjs/vite-plugin-federation). All Javascript frameworks that are supported by Vite can be used, including Vue, React, Svelte, and more. The path must point towards a remote entry point. This is an experimental feature and can be subject to errors.

The component will be available on the frontend through the route `/<extension.name>/<component.name>`. For example, the component registered above will be available at `/my-extension/my-component` and will display an iframe to `https://example.com`.

A [menu item](menus.md) or [dashboard button](dashboards.md) can be used to create an internal link to this route.

## Reference

:::collectivo.components.models.Component
