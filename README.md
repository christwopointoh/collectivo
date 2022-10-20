# collectivo

A Django package. Using [collectivo-ux](https://github.com/MILA-Wien/collectivo-ux/) as a frontend.

## Development

Requirements for the development environment that is used in our team:

1. [Docker](https://www.docker.com/), Version 20.10.
2. [VisualStudioCode](https://code.visualstudio.com/) (VSCode) with the extension "Django".

To run and test the app with docker:

- To build the micro-frontend components (TODO: Perform this with docker build):
    - Move to `cd collectivo-test-app/test_extension/ux_component`
    - Run `yarn`
    - Run `yarn build`
- To build a development server, run: `docker compose build`
- To run a development server:
    - If you want to develop just the backend, run: `docker compose up -d`
    - If you also want to develop the frontend, run `docker compose up -d collectivo db keycloak` and follow the instructions at [collectivo-ux](https://github.com/MILA-Wien/collectivo-ux/) to set up a development server for the frontend.
- To perform tests and linting, run: `docker compose run --rm collectivo sh -c "python manage.py test && flake8"`

## Documentation

- The API will be available at http://127.0.0.1:8000/.
- The API documentation will be available at `/api/docs/`.
- To test the frontend, you can use the API call `GET` at `/api/version/`.
- To test backend and frontend together, see [collectivo-ux](https://github.com/MILA-Wien/collectivo-ux).
- To export the keycloak realm including users run `docker compose exec -u 0 keycloak /opt/keycloak/bin/kc.sh export --dir /tmp/export --realm collectivo --users realm_file` Note: exporting the realm via the gui doesn't include the users. The exported files is then in the `./docker/keycloak/export` folder.
