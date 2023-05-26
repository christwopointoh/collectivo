# Reference

## Backend Settings

### Core

Custom settings for Collectivo can be set in `collectivo.yml`.

Environment variables can be used with the `${ENV_VAR_NAME}` syntax.

The following settings can be set:

`db_name` (string)

: Name of the database.

`db_host` (string)

: Hostname of the database.

`db_user` (string)

:  Username of the database.

`db_pass` (string)

: Password of the database.

`secret_key` (string)

: Secret key for the Django app.

`allowed_hosts` (list)

: List of allowed hostnames of collectivo.

`allowed_origins` (list)

: List of allowed URLs that can send requests to collectivo.


`extensions` (list)

: Extensions that should be installed (list).

    Extensions can be added from three sources:

    - Built-in modules of collectivo
    - Modules placed in the ./extensions directory
    - Packages installed via requirements.txt

`development` (boolean)

: Activate development tools and debugging messages.

    !!! warning "Warning"

        Do not activate this setting on a production system, not even temporarily.
        It is possible to extract secrets from the system if this setting is activated.

`example_data` (boolean)

: Populate the instance with example data.

`api_docs` (boolean)

: Activate [Swagger UI](https://swagger.io/tools/swagger-ui/) under `/api/docs`


### Extensions

Each extension can have a file `extensions.yml` in its root folder,
that will be used as default configuration variables for that extension.

The following standard extension settings can be used:

`authentication_classes` (list)

: Default [authentication classes](https://www.django-rest-framework.org/api-guide/authentication/#setting-the-authentication-scheme) to be added to the Django REST framework.

`user_admin_serializer` (str)

: A serializer class whose fields will be added to the `core/users` view.

## Frontend Settings

### Core

Custom settings for the Collectivo frontend can be set in `src/collectivo.json`.
A new build is necessary for these settings to be applied.

The following settings can be set:

`extensions` (list)

: Name of extensions to be included. The name must match the name of the extension folder in `src/extensions`. If the extension folder contains a file `extension.ts`
with a default export function, this function will automatically be called before
the app is started.

### Extensions

Each frontend extension can have a file `extensions.json` in its root folder,
that will be used as default configuration variables for that extension.

The following standard extension settings can be used:

`endpoints` (dict)

: Name and path of endpoints to be added to the API and main store.

`profile_admin_endpoints` (list)

: Names of endpoints that should be used for the `/core/users/:id` view.

`profile_user_endpoints` (list)

: Names of endpoints that should be used for the `/core/profile` view.
