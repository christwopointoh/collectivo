# User guide

Step-by-step instructions on how to use Collectivo.

## Installation

To install Collectivo, follow these steps:

- Install [Docker](https://docs.docker.com/get-docker/) (Version >= 20.10)

- Clone the collectivo quickstart repository and set up a fresh environment file.

    ```sh
    git clone https://github.com/MILA-Wien/collectivo-quickstart .
    cp .env.example .env
    ```

## Local instance

To run a local instance of Collectivo, follow these steps:

- Follow the [installation](guide.md#installation) instructions.
- Add the following line to your [hosts file](https://www.howtogeek.com/27350/beginner-geek-how-to-edit-your-hosts-file/):

    ```title="etc/hosts"
    127.0.0.1 keycloak
    ```

- Optional: Define a version of Collectivo in `collectivo/Dockerfile` and `collectivo-ux/Dockerfile-dev`.
- Run `docker compose up -d` to start the server.
- Run `docker compose build --no-cache --pull` to build fresh images.
- You can now go to [`127.0.0.1:8001`](http://127.0.0.1:8001) and log in to Collectivo as `test_superuser@example.com` with the pasword `Test123!`.

## Configuration

To configure collectivo, follow these steps:

- Follow the [installation](guide.md#installation) instructions.
- Change the backend settings in [`collectivo/collectivo.yml`](reference.md#backend-settings).
- Change the frontend settings in [`collectivo-ux/collectivo.json`](reference.md#frontend-settings).
    - Set a new favicon as `collectivo-ux/favicon.ico`

## Deployment

To deploy collectivo, follow these steps:

- Follow the [installation](guide.md#installation) instructions.
- Create separate DNS entries to your server for backend, frontend, and keycloak.
- Define your server settings and secret vars in `.env`.
- Run `docker-compose -f ./docker-compose.prod.yml up -d keycloak` to start keycloak.
- Go to your keycloak URL and log in to the admin console. Then go to the realm `collectivo` - `Clients` - `collectivo` - `Credentials`, generate a new client secret and put it in your `.env` file as `COLLECTIVO_KEYCLOAK_CLIENT_SECRET`.
- Define a version of Collectivo in `collectivo/Dockerfile` and `collectivo-ux/Dockerfile`.
- Run `docker compose -f ./docker-compose.prod.yml build --no-cache --pull` to build fresh images.
- Run `docker compose -f ./docker-compose.prod.yml up -d` to start the server.
