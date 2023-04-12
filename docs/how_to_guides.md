# How-to Guides

## How to set up a local development enviroment

### Set up the backend

Docker is required to set up the development environment for the backend.

To set up a development system of collectivo on your local machine:

- Install docker and docker-compose (Version >= 20.10)
- Clone the repository with `git clone https://github.com/MILA-Wien/collectivo.git`
- Copy `.env.example` and rename it to `.env`
- Add the following line to your `/etc/hosts/` file: `127.0.0.1 keycloak collectivo.local`
- Start a local instance of collectivo with `docker compose up -d`
- Perform tests and linting with `docker compose run --rm collectivo sh -c "python manage.py test && flake8"`

The development system will be accessible via the following paths:

- Backend (API docs): `http://collectivo.local:8000/api/docs/`
- Keycloak (Console): `http://keycloak:8080/admin/master/console/`

### Set up the frontend

If you want to develop only the backend, you can skip this step
and access the latest version of the frontend
via `http://collectivo.local:8001`.

If you want to develop the frontend (collectivo-ux),
you need npm, nodejs, and yarn -
which can be installed with `npm install -g yarn`.

To set up a development system of collectivo-ux on your local machine:

1. Add a CORS-disabler Add-On to your browser e.g. [CORS Everywhere](https://addons.mozilla.org/en-US/firefox/addon/cors-everywhere/) for Firefox or [Allow CORS](https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf) for Chrome and start it in development mode
2. In your terminal, run `yarn dev`
3. The frontend is now available via `collectivo.local:5173`

### Test the local system

Open the frontend in your browser (see above) and use one of the following
test users to explore the development system:

- `test_superuser@example.com`
- `test_member_01@example.com`, `test_member_02@example.com`, `test_member_03@example.com`
- `test_user_not_verified@example.com`
- `test_user_not_member@example.com`

The password for all users is `Test123!`.
