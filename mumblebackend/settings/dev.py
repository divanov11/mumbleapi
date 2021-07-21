from mumblebackend.settings.base import *
from .base import *
import os
# override base.py settings

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'message': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'messages.sqlite3',
    }
}


DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage' 