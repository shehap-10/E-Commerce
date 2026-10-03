from .base import *  # noqa: F403

from django.core.exceptions import ImproperlyConfigured

if ENVIRONMENT != "production":
    raise ImproperlyConfigured("Set ENVIRONMENT=production to use prod settings.")

DEBUG = False
