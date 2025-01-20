import os

import sentry_sdk
from config.util import strtobool
from config.versioning import get_git_sha
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration

if SENTRY_DSN := os.getenv("SENTRY_DSN", ""):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=os.getenv("ENVIRONMENT_NAME", "production"),
        release=get_git_sha(),
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=strtobool(os.getenv("SENTRY_SEND_USER_DATA", "False")),
    )
