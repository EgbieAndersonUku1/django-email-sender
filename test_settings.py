import os
from django.conf.global_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'dummy-key'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_email_sender',  
    
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

LOGGING_CONFIG = None
LOGGING = {}

FORCE_SCRIPT_NAME = None
