"""Local Development settings."""

from .base import *  # NOQA
from .base import env
import os

# Base
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-c-#)%lu-_=uf6$x!p$-ecoiu20+^ile&x-fqp3)jttk4!q4$@j",
)
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "10.0.2.2",  # localHost for android emulator
    "host.docker.internal",  # Admin Local
]

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# Templates
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # NOQA

RUN_MAIN = os.getenv("RUN_MAIN")
