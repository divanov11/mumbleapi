from .base import *

import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

sentry_sdk.init(
    dsn="https://de808f6f605c4fd79120ddb21f073904@o599875.ingest.sentry.io/5743882",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('MUMBLE_DB_NAME'),
        'USER': os.environ.get('MUMBLE_USER'),
        'PASSWORD': os.environ.get('MUMBLE_DB_PASS'),
        'HOST': os.environ.get('MUMBLE_HOST'),
        'PORT': '5432',
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

LINODE_BUCKET = 'mumble'
LINODE_BUCKET_REGION = 'us-east-1'
LINODE_BUCKET_ACCESS_KEY = os.environ.get('MUMBLE_LINODE_BUCKET_ACCESS_KEY')
LINODE_BUCKET_SECRET_KEY = os.environ.get('MUMBLE_LINODE_BUCKET_SECRET_KEY')

AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False

AWS_S3_ENDPOINT_URL = f'https://{LINODE_BUCKET_REGION}.linodeobjects.com'
AWS_ACCESS_KEY_ID = LINODE_BUCKET_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = LINODE_BUCKET_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = LINODE_BUCKET

django_heroku.settings(locals(), test_runner=False)
