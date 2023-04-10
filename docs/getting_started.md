# Getting started

Collectivo is an open-source framework for participative community platforms.
It provides a modular structure that makes it is easy to customize for
the needs of different organisations.

## Installation

There are two ways to install collectivo:

- You can install collectivo as a complete application using Docker.
- You can add collectivo as a Python package to an existing Django project.

### Installation using Docker

!!! warning "Work in progress"

    The collectivo-quickstart repository doesn't exist yet.

Install Docker from [here](https://docs.docker.com/get-docker/).

Then, open the terminal inside a folder for your
project and enter the following:

```sh
git clone https://github.com/MILA-Wien/collectivo-quickstart
cd collectivo
docker compose up -d
```

### Installation using Django

!!! warning "Work in progress"

    The collectivo PyPi package does not yet include the latest release.

Add `collectivo` to the requirements of an existing Django project.
Adopt the settings of your Django project based on the default settings of
collectivo that can be found
[here](https://github.com/MILA-Wien/collectivo/blob/main/collectivo_app/collectivo_app/settings.py).
