from decouple import config

from .base import *

SECRET_KEY = config("SECRET_KEY")

DEBUG = True

INSTALLED_APPS += ("django_extensions",)

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# django-allauth

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "123",
            "secret": "456",
            "key": "",
        },
    },
}
