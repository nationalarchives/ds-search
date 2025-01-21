import os

from .base import *
from .features import *

CACHE_HEADER_DURATION = int(
    os.environ.get("CACHE_HEADER_DURATION", "604800")
)  # 1 week

# TODO: This invalidates the CSP nonces
CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "300"))
