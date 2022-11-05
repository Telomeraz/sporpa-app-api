from .base import *

DEBUG = True

INSTALLED_APPS.append("django_extensions")


# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
