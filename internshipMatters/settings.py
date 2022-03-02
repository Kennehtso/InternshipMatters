"""
Django settings for internshipMatters project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

import environ
env = environ.Env()
environ.Env.read_env() # reading .env file

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'grr+&ow&z62lq+d($0d+2)y3uwrnd58_lwi3%cs@bvu6#gcm61'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['internships-matters.herokuapp.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'general.apps.GeneralConfig',
    "storages",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'internshipMatters.urls'

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

WSGI_APPLICATION = 'internshipMatters.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
     'ENGINE': 'django.db.backends.postgresql',
    }
   }
DATABASES['default'].update(env.db())
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
#Static Root for collectstatic
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


if not DEBUG:
    #print(f"env.db(): {env.db()}")
    ALLOWED_HOSTS= ['*']
    #import dj_database_url
    #format as: postgress://user:password@HOST:port/Database。
    #defaulturl = f'postgres://{os.environ.get("internshipMatters_user")}:{os.environ.get("internshipMatters_pw")}@{os.environ.get("internshipMatters_db")}:{os.environ.get("internshipMatters_port")}/{os.environ.get("internshipMatters_db_name")}'
    #print(F"defaulturl: {defaulturl}")
    #db_from_env = dj_database_url.config(env = defaulturl, default=defaulturl)
    #print(F"DATABASE_URL: {db_from_env}")
    DATABASES['default'].update(env.db())

    #AWS S3 Connetction
    """
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/' #'static/'
    AWS_S3_REGION_NAME ="ap-northeast-3"

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/' #'static/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
    """
# Customize Added
STATICFILES_DIRS = [
    #BASE_DIR / "static",
    Path.joinpath(BASE_DIR, STATIC_URL),
    Path.joinpath(BASE_DIR, MEDIA_URL)
]

# SMTP Config
SENDGRID_API_KEY = env('SEND_GRID_API_KEY')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = 'smtp.sendgrid.net'
#EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_USER = 'apikey' 
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True


#Whitenoise static files handling
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

import logging
from logging.handlers import SysLogHandler
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        # Warning messages are sent to admin emails
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        # critical errors are logged to sentry
        'sentry': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'mail_admins', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}