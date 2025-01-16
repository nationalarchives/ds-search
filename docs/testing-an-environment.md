# Testing an environment

## 1. Trigger an error

1. Update the `SENTRY_DEBUG_URL_ENABLED` env var to `True` for the environment and restart the container.
2. When the service is available again, visit the `/sentry-debug/` URL in your browser to trigger a `ZeroDivisionError`.
3. Log into [Sentry](https://sentry.io/organizations/the-national-archives/projects/) and check the relevant project for a new issue event with an `environment` value matching the `SENTRY_ENVIRONMNET` env var value set for the environment.
4. Once confirmed that Sentry is working, update the `SENTRY_DEBUG_URL_ENABLED` env var to `False` for the environment, and restart the container.
