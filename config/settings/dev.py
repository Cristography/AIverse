

"""
Development settings - used when running locally
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Development-only apps
INSTALLED_APPS += [
    # Add django-debug-toolbar here if you want
]

# Show emails in console during development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
