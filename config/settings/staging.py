import os

from .base import *
from .features import *

# TODO: This invalidates the CSP nonces
CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "60"))

# sentry settings
try:
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "0.25"))
    from .sentry import *
except ImportError:
    pass
