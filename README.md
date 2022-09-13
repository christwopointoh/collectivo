# MachMit Kern Backend

Dockerized Django REST API with a PostgreSQL database.

Based on https://github.com/LondonAppDeveloper/recipe-app-api

To build the container, run: `docker-compose build`

To start the project, run: `docker-compose up`

The API will then be available at http://127.0.0.1:8000/

The API documentation will be available at http://127.0.0.1:8000/api/docs/

To test the frontend, you can use the API call `GET` at `/api/core/version/"`.

To perform tests and linting, run: `docker-compose run --rm app sh -c "python manage.py test && flake8"`
