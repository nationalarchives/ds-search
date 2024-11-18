import os

from config.util import strtobool

from .base import *
from .features import *

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

DEBUG = strtobool(os.getenv("DEBUG", "True"))

# for develop only set default False
CLIENT_VERIFY_CERTIFICATES = strtobool(
    os.getenv("CLIENT_VERIFY_CERTIFICATES", "False")
)

FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "False"))

DJANGO_SERVE_STATIC = True

if not DEBUG and DJANGO_SERVE_STATIC:
    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )

if DEBUG:

    INSTALLED_APPS += [  # noqa: F405
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE  # noqa: F405

    def show_toolbar(request) -> bool:
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        "SHOW_COLLAPSED": True,
    }
