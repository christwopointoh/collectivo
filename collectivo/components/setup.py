"""Setup function for the components module."""

from django.conf import settings

from collectivo.extensions.apps import ExtensionsConfig
from collectivo.extensions.models import Extension
from collectivo.menus.models import Menu, MenuItem

from .models import Component


def setup(sender, **kwargs):
    """Initialize extension after database is ready."""

    extension = Extension.register(
        name=ExtensionsConfig.name,
        description=ExtensionsConfig.description,
        built_in=True,
    )

    if settings.COLLECTIVO["example_data"] is True:
        # Remote entries
        Component.register(
            name="component1",
            type="remote",
            path="http://localhost:4173/assets/disposerv.js",
            extension=extension,
        )
        Component.register(
            name="component2",
            type="remote",
            path="http://localhost:4172/assets/disposerv.js",
            extension=extension,
        )
        Component.register(
            name="component3",
            type="iframe",
            path="http://localhost:4172",
            extension=extension,
        )

        MenuItem.register(
            name="remote1",
            label="Remote 1",
            extension=extension,
            parent="admin",
            route=extension.name + "/component1",
            requires_perm=("admin", "core"),
            order=200,
        )
        MenuItem.register(
            name="remote2",
            label="Remote 2",
            extension=extension,
            parent="admin",
            route=extension.name + "/component2",
            requires_perm=("admin", "core"),
            order=200,
        )
        MenuItem.register(
            name="remote3",
            label="Remote 3",
            extension=extension,
            parent="admin",
            route=extension.name + "/component3",
            requires_perm=("admin", "core"),
            order=200,
        )
