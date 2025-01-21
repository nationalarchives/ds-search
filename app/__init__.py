import sentry_sdk
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT_NAME,
        release=settings.BUILD_VERSION,
        integrations=[DjangoIntegration()],
        sample_rate=settings.SENTRY_SAMPLE_RATE,
        traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
        profiles_sample_rate=settings.SENTRY_SAMPLE_RATE,
    )
