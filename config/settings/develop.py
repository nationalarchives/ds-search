import os

from config.util import strtobool

from .base import *
from .features import *

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = INSTALLED_APPS + [  # noqa: F405
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa: F405

DEBUG = strtobool(os.getenv("DEBUG", "True"))

FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "False"))
