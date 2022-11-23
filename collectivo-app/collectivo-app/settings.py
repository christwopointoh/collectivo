"""Django settings for collectivo-app."""
import os
from pathlib import Path
from collectivo.version import __version__

# TODO FOR PRODUCTION
# Go through https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# Change allowed_hosts
# Remove unused django functions

# Try to import custom settings
try:
    from extensions import settings
    _custom_settings = vars(settings)
except ModuleNotFoundError:
    _custom_settings = {}

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', False)
DEVELOPMENT = os.environ.get('DEVELOPMENT', False)

if os.environ.get('ALLOWED_HOSTS') is not None:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').replace(' ', '').split(',')
elif DEVELOPMENT:
    ALLOWED_HOSTS = ['*',"0.0.0.0","127.0.0.1", "localhost", "testserver"]
else:
    ALLOWED_HOSTS = []

# Install built-in collectivo extensions
_built_in_extensions = [
    f'collectivo.{ext}' for ext in
    os.environ.get('COLLECTIVO_EXTENSIONS', '').replace(' ', '').split(',')
]

INSTALLED_APPS = [
    *_custom_settings.get('INSTALLED_APPS_TOP', []),
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'collectivo',
    'django_filters',
    'rest_framework',
    'drf_spectacular',
    *_built_in_extensions,
    *_custom_settings.get('INSTALLED_APPS', [])
]

MIDDLEWARE = [
    *_custom_settings.get('MIDDLEWARE_TOP', []),
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'collectivo.auth.middleware.KeycloakMiddleware',
    *_custom_settings.get('MIDDLEWARE', [])
]

if DEVELOPMENT:
    INSTALLED_APPS += ['collectivo.devtools', 'corsheaders']
    MIDDLEWARE += ['corsheaders.middleware.CorsMiddleware']
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

ROOT_URLCONF = 'collectivo-app.urls'

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

WSGI_APPLICATION = 'collectivo-app.wsgi.application'


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

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.environ.get('TIME_ZONE', 'CET')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.realpath(os.path.join(BASE_DIR, 'static'))


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django Rest Framework (DRF)
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ]
}


# DRF Spectacular (OpenAPI)
# https://drf-spectacular.readthedocs.io/

_schema_versions = ['0.1.0']
_swagger_urls = ''
for version in _schema_versions:
    _swagger_urls += (
        f'{{url: "/api/collectivo/schema/?version={version}", '
        f'name: "API Version {version}"}}, '
    )
print(_swagger_urls)

SPECTACULAR_SETTINGS = {
    'TITLE': 'collectivo',
    'DESCRIPTION': 'A modular framework to build participative community platforms.',
    'LICENSE': {
        'name': 'GNU Affero General Public License v3.0',
        'url': 'https://github.com/MILA-Wien/collectivo/blob/main/LICENSE'
    },
    'VERSION': '',
    'SERVERS': [],
    'TAGS': [],
    'EXTERNAL_DOCS': {'url': 'https://github.com/MILA-Wien/collectivo'},

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

    # Define SWAGGER UI with top bar for version switching
    'SWAGGER_UI_SETTINGS':  f'''{{
        deepLinking: true,
        urls: [{_swagger_urls}],
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
        layout: "StandaloneLayout",
        persistAuthorization: true,
        filter: true
    }}'''
}


# Logging
# https://docs.djangoproject.com/en/4.1/ref/logging/

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


# Settings for collectivo

COLLECTIVO = {
    # Path to default models
    'default_auth_manager': 'collectivo.auth.manager.KeycloakAuthManager',
    'default_user_model': 'collectivo.members.models.Member',
    'default_extension_model': 'collectivo.extensions.models.Extension',

    **_custom_settings.get('COLLECTIVO', {})
}


# Configuration for collectivo.auth.middleware.KeycloakMiddleware
KEYCLOAK = {
    'SERVER_URL': os.environ.get('KEYCLOAK_SERVER_URL'),
    'REALM_NAME': os.environ.get('KEYCLOAK_REALM_NAME', 'collectivo'),
    'CLIENT_ID': os.environ.get('KEYCLOAK_CLIENT_ID', 'collectivo'),
    'CLIENT_SECRET_KEY': os.environ.get('KEYCLOAK_CLIENT_SECRET_KEY')
}



