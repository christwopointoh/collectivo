# Reference

## Settings

Custom installation settings for Collectivo can be set in `collectivo.yml`,
in the root folder of the collectivo app.

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


## Extension settings

Each extension can have a file `extensions.yml` in its root folder,
that will be used as default configuration variables for that extension.
The following standard extension settings can be used:

`authentication_classes` (list)

: Default [authentication classes](https://www.django-rest-framework.org/api-guide/authentication/#setting-the-authentication-scheme) to be added to the Django REST framework.

`user_admin_serializer` (str)

: A serializer class whose fields will be added to the `core/users` view.
