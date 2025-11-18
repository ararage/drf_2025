"""Live settings."""

from .base import *  # NOQA
import os

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])

# Databases
DATABASES["default"] = env.db("DATABASE_URL")  # NOQA
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # NOQA
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=0)  # NOQA


# Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

# Gunicorn
INSTALLED_APPS += ["gunicorn"]  # noqa F405

# WhiteNoise
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa F405

# Logging info fro rottaing files.
LOGFILE_DIR = os.environ.get("LOG_DIR", BASE_DIR)
LOGFILE_ERROR = LOGFILE_DIR + "_errors.log"
LOGFILE_GENERAL = LOGFILE_DIR + "_general.log"
LOGFILE_SIZE = 1 * 1024 * 1024
LOGFILE_COUNT = 2

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
        "django.db": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.template": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "users": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
    },
}
