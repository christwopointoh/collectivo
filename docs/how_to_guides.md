# How-to Guides

## How to set up a local development system

### Backend

Docker is required to set up the development environment for the backend.

To set up a development system of collectivo:

- Install docker and docker-compose (Version >= 20.10)
- Clone the repository with
  `git clone https://github.com/MILA-Wien/collectivo.git`
- Copy `.env.example` and rename it to `.env`
- Add the following line to your `/etc/hosts/` file:
  `127.0.0.1 keycloak collectivo.local`
- Start a local instance of collectivo with `docker compose up -d`
- Perform tests and linting with
  `docker compose run --rm collectivo sh -c "python manage.py test && flake8"`

### Frontend (optional)

To set up a development system of collectivo-ux, you need to install [yarn](https://classic.yarnpkg.com/lang/en/docs/install/) and run:

```sh
git clone https://github.com/MILA-Wien/collectivo-ux.git
cd collectivo-ux
yarn
yarn dev
```

To perform end-to-end tests, run:

```sh
yarn build:staging
yarn test:e2e
```

### Access the system

You can now access the following pages in your browser:

- Frontend (collectivo-ux):
    - Development `http://localhost:5173`
    - Normal `http://localhost:8001`
- Keycloak: `http://keycloak:8080/admin/master/console/`
- Documentation: `http://localhost:8003`
- API Docs (Swagger): `http://localhost:8000/api/docs/`

### Example users

If example_data is activated, you can log in with the following users:

- `test_superuser@example.com`
- `test_member_01@example.com`, `test_member_02@example.com`,
  `test_member_03@example.com`
- `test_user_not_verified@example.com`
- `test_user_not_member@example.com`

The password for all users is `Test123!`.
