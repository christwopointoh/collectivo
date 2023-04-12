# Reference

## Settings file

Custom installation settings for Collectivo can be set in `collectivo.yml`,
which should be placed into the root folder of the collectivo app.

The following settings can be set:

`extensions`

: Extensions that should be installed (list).

    Extensions can be added from three sources:

    - Built-in modules of collectivo
    - Modules placed in the ./extensions directory
    - Packages installed via requirements.txt

`development`

: Activate development tools and debugging messages (boolean).

    !!! warning "Warning"

        Do not activate this setting on a production system, not even temporarily.
        It is possible to extract secrets from the system if this setting is activated.

`example_data`

: Populate the instance with example data (boolean).
