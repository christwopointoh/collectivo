"""Django settings for collectivo-test-app."""
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%x_1s#a=mf9rfm+@waioqu@)(2o5s3ff&*f0gas-$*8%#9kj7%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEVELOPMENT = True

ALLOWED_HOSTS = ['*',"0.0.0.0","127.0.0.1", "localhost", "testserver"]

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'collectivo',
    'collectivo.menus',
    'collectivo.dashboard',
    'collectivo.auth',
    'collectivo.extensions',
    'collectivo.members',

    'test_extension',

    'django_filters',
    'rest_framework',
    'drf_spectacular',

    'corsheaders',  # TODO DEBUG
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # TODO DEBUG

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'collectivo.auth.middleware.KeycloakMiddleware',
]

ROOT_URLCONF = 'collectivo-test-app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'collectivo-test-app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_DIR = os.path.realpath(os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.realpath(os.path.join(BASE_DIR, 'static'))


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS Settings - TODO Remove?

CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]
CORS_ORIGIN_ALLOW_ALL = True


# Django Rest Framework (DRF)

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ]
}


# DRF Spectacular (OpenAPI)

SPECTACULAR_SETTINGS = {
    # Allow for authentication via token in the SwaggerUI interface
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
            }
        }
    },
    "SECURITY": [{"ApiKeyAuth": [], }],
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timeandname': {
            'format': '[{name}] {message}',  # {asctime},
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': 'dataflair-debug.log',
        # },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'timeandname',
        },
    },
    'loggers': {
        'collectivo': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'test_extension': {
            'handlers': ['console'],  # 'file',
            'level': 'DEBUG',  # os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
            'propagate': True,
        },
    },
}


# General settings for collectivo

COLLECTIVO = {

    # Define user groups and their respective roles
    'auth_groups_and_roles': {
        'members': ['members_user'],
        'members_active': ['shifts_user'],
        'superusers': ['collectivo_admin', 'members_admin', 'shifts_admin']
    },

    # Configuration for auth.middleware.KeycloakMiddleware
    'auth_keycloak_config': {
        'SERVER_URL': 'http://keycloak:8080',
        'REALM_NAME': 'collectivo',
        'CLIENT_ID': 'collectivo',
        'CLIENT_SECRET_KEY': '**********'
    },

    # Path to default models
    'default_auth_manager': 'collectivo.auth.manager.KeycloakAuthManager',
    'default_user_model': 'collectivo.members.models.Member',
    'default_extension_model': 'collectivo.extensions.models.Extension',

}





