"""
Django settings for this project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
from environs import Env
from unipath import Path

env = Env()
env.read_env()  # read .env file, if it exists

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = Path(__file__).parent.parent.parent
BASE_DIR = Path(__file__).parent.parent
ENVIRONMENT = os.environ.get('ENVIRONMENT_TYPE', 'localdev')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# The SECRET_KEY is provided via an environment variable in OpenShift
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    default='9e4@&tw46$l31)zrqe3wi+-slqm(ruvz&se0^%9#6(_w3ui!c0'
)

DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'debug_toolbar',
    'corsheaders',
    'edivorce.apps.core',
    'compressor',
    'crispy_forms',
    'sass_processor',
)

# add the POC app only if applicable
if ENVIRONMENT in ['localdev', 'dev', 'test', 'minishift']:
    INSTALLED_APPS += (
        'edivorce.apps.poc',
    )

MIDDLEWARE = (
    'edivorce.apps.core.middleware.basicauth_middleware.BasicAuthMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edivorce.apps.core.middleware.bceid_middleware.BceidMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

ROOT_URLCONF = 'edivorce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['edivorce/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'edivorce.apps.core.context_processors.settings_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# need to disable auth in Django Rest Framework so it doesn't get triggered
# by presence of Basic Auth headers
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'edivorce.apps.core.authenticators.BCeIDAuthentication',
    ]
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_TZ = True
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True
USE_THOUSANDS_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

BCGOV_NETWORK = os.environ.get('PROXY_NETWORK', '0.0.0.0/0')

FORCE_SCRIPT_NAME = '/'

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'edivorce', 'fixtures'),
)

BASICAUTH_ENABLED = False

# Google Tag Manager (dev/test instance)
GTM_ID = 'GTM-NJLR7LT'


def show_toolbar(request):
    return ENVIRONMENT in ['localdev', 'dev', 'minishift']


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    'SHOW_COLLAPSED': True,
}

SECURE_BROWSER_XSS_FILTER = True

LOGOUT_URL = '/accounts/logout/'

# CLAMAV settings

# eFiling Hub settings
EFILING_HUB_TOKEN_BASE_URL = env('EFILING_HUB_TOKEN_BASE_URL', 'https://efiling.gov.bc.ca')
EFILING_HUB_REALM = env('EFILING_HUB_REALM', 'abc')
EFILING_HUB_CLIENT_ID = env('EFILING_HUB_CLIENT_ID', 'abc')
EFILING_HUB_CLIENT_SECRET = env('EFILING_HUB_CLIENT_SECRET', 'abc')
EFILING_HUB_API_BASE_URL = env('EFILING_HUB_API_BASE_URL', 'https://efiling.gov.bc.ca')

EFILING_BCEID = env.dict('EFILING_BCEID', '', subcast=str)
