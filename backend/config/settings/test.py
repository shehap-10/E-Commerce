from .base import *  # noqa: F403

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecommerce",
        "USER": "ecommerce",
        "PASSWORD": "ecommerce_dev_only",
        "HOST": "db",
        "PORT": "5432",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]