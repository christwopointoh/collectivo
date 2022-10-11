# Use Python runtime as parent image
FROM python:3.9-alpine3.13

# Send stdout and sterr messages directly to the terminal
ENV PYTHONUNBUFFERED 1

# Install temporary packages to build the postgresql database
RUN apk add --update --no-cache postgresql-client  && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev

# Copy further requirements into the container
COPY ./requirements.txt /tmp/requirements.txt

# Copy source code of the test app into the container
COPY ./collectivo-test-app /collectivo-test-app

# Copy source code of the collectivo app into the test app
COPY ./collectivo /collectivo-test-app/collectivo

# Move working directory into the test app
WORKDIR /collectivo-test-app

# Set port through which the test app can be accessed
EXPOSE 8000

# Install requirements and remove temporary files
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

# Remove temporary packages and create a new user
RUN apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

# TODO What does this do?
ENV PATH="/py/bin:$PATH"

# Set new user (this prevents root access to the server)
USER django-user

# Set default command
CMD while ! nc -z db 5432; do sleep 1; done && \
             python manage.py migrate && \
             python manage.py runserver 0.0.0.0:8000
