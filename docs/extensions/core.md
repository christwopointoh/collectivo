# Core

Manage users, permissions, and core settings. This extension is required for Collectivo to function.

## Installation

Add `collectivo.core` to `extensions` in [`collectivo.yml`](reference.md#settings).

## Usage

### Edit profiles

Users can edit their profiles in the section `Profile`. This section displays the registered profile models of all extensions.

### Manage user profiles

User data can be managed in the section `Users - Users`. This section displays the registered profile models of all extensions.

### Assign permissions to users

Permission can be managed in the section `Users - Groups`.
Permissions are assigned through permission groups. To assign a permission to a user, first add this permission to a permission group, and then add the user to this group.

## Reference

:::collectivo.core.models.Permission
    options:
        members: None

:::collectivo.core.models.PermissionGroup
    options:
        members: None

:::collectivo.core.models.CoreSettings
    options:
        members: None
