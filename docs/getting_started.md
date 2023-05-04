# Getting started

Collectivo is an open-source membership platform for communities and collectives.
It is designed with a modular structure that makes it easy to customize and extend
the platform for the needs of different organisations and integrate
multiple tools into a single application.

This tutorial shows you how to quickly set up your own instance of Collectivo
together with an instance of [Keycloak](https://www.keycloak.org/) that we will use to handle authentication.

## Requirements

This tutorial requires Docker. You can install it [here](https://docs.docker.com/get-docker/).

To be able to use Keycloak locally, you further need to add the following line to your hosts file:

```title="etc/hosts"
127.0.0.1 keycloak collectivo.local
```

## Installation

Open a terminal inside an empty folder for your project and run the following commands:

```sh
git clone https://github.com/MILA-Wien/collectivo-quickstart .
cp .env.example .env
docker compose up -d
```

This will clone the collectivo-quickstart repository into your folder,
create a default environment file for your project, and install a local instance of Keycloak and Collectivo.

## Try it out

You can now go to `collectivo.local:8001` to try out your local instance of Collectivo.

The following example users can be used to log in on your platform:

- `test_superuser@example.com`
- `test_member_01@example.com`, `test_member_02@example.com`, `test_member_03@example.com`
- `test_user_not_verified@example.com`
- `test_user_not_member@example.com`

The password for all users is `Test123!`.
