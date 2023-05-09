# Getting started

This tutorial will show you how to quickly set up your own instance of Collectivo.

## Installation

Install the following requirements:

- [Docker](https://docs.docker.com/get-docker/) (Version >= 20.10)

Add the following line to your [hosts file](https://www.howtogeek.com/27350/beginner-geek-how-to-edit-your-hosts-file/):

```title="etc/hosts"
127.0.0.1 keycloak
```

In your project folder, clone the collectivo quickstart repository and start a local instance of collectivo:

```sh
git clone https://github.com/MILA-Wien/collectivo-quickstart .
cp .env.example .env
docker compose up -d
```

## Try it out

You can now go to [`127.0.0.1:8001`](http://127.0.0.1:8001) to log in to Collectivo.

The following example users can be used to log in on your platform:

- `test_superuser@example.com`
- `test_member_01@example.com`, `test_member_02@example.com`, `test_member_03@example.com`
- `test_user_not_verified@example.com`
- `test_user_not_member@example.com`

The password for all users is `Test123!`.
