import os

from config.util import strtobool

from .base import *
from .features import *

DEBUG = strtobool(os.getenv("DEBUG", "True"))

FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "False"))
