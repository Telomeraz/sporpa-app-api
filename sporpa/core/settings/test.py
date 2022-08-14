from decouple import config

from .base import *

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

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


# Email Settings

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
