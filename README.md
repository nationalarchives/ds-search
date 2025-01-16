# TNA Python Django Search Application

## Setting up a local build

Local development is done in Docker.

### Before starting a build for the first time

```sh
cp .env.example .env
```

`.env` hold sensitive values. Please ask on the `ds-etna-dev` slack channel to get those values.

### Build and start the container

```sh
docker compose up -d
```

### Add the static assets

During the first time install, your `app/static/assets` directory will be empty.

As you mount the project directory to the `/app` volume, the static assets from TNA Frontend installed inside the container will be "overwritten" by your empty directory.

To add back in the static assets, run:

```sh
docker compose exec app cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets /app/app/static
```

### Preview application

<http://localhost:65533/>

### Preview docs

<http://localhost:65532/>

### Run tests

```sh
docker compose exec dev poetry run python manage.py test
```

### Format and lint code

```sh
docker compose exec dev format
```

## Environment variables

In addition to the [base Docker image variables](https://github.com/nationalarchives/docker/blob/main/docker/tna-python-django/README.md#environment-variables), this application has support for:

| Variable                          | Purpose                                                   | Default                      |
| --------------------------------- | --------------------------------------------------------- | ---------------------------- |
| `DJANGO_SETTINGS_MODULE`          | The configuration to use                                  | `config.settings.production` |
| `DEBUG`                           | If true, allow debugging                                  | `False`                      |
| `COOKIE_DOMAIN`                   | The domain to save cookie preferences against             | _none_                       |
| `DATABASE_NAME`                   | The name of the Postgres database                         | _none_                       |
| `DATABASE_USER`                   | The username needed to access the Postgres database       | _none_                       |
| `DATABASE_PASSWORD`               | The password needed to access the Postgres database       | _none_                       |
| `DATABASE_HOST`                   | The Postgres database host                                | _none_                       |
| `DATABASE_PORT`                   | The Postgres database port                                | `5432`                       |
| `CSP_IMG_SRC`                     | A comma separated list of CSP rules for `img-src`         | `'self'`                     |
| `CSP_SCRIPT_SRC`                  | A comma separated list of CSP rules for `script-src`      | `'self'`                     |
| `CSP_SCRIPT_SRC_ELEM`             | A comma separated list of CSP rules for `script-src-elem` | `'self'`                     |
| `CSP_STYLE_SRC`                   | A comma separated list of CSP rules for `style-src`       | `'self'`                     |
| `CSP_STYLE_SRC_ELEM`              | A comma separated list of CSP rules for `style-src-elem`  | `'self'`                     |
| `CSP_FONT_SRC`                    | A comma separated list of CSP rules for `font-src`        | `'self'`                     |
| `CSP_CONNECT_SRC`                 | A comma separated list of CSP rules for `connect-src`     | `'self'`                     |
| `CSP_MEDIA_SRC`                   | A comma separated list of CSP rules for `media-src`       | `'self'`                     |
| `CSP_WORKER_SRC`                  | A comma separated list of CSP rules for `worker-src`      | `'self'`                     |
| `CSP_FRAME_SRC`                   | A comma separated list of CSP rules for `frame-src`       | `'self'`                     |
| `GA4_ID`                          | The Google Analytics 4 ID                                 | _none_                       |
| `ROSETTA_API_VERIFY_CERTIFICATES` | Verify certificate for API                                | `True`                       |
| `SENTRY_DEBUG_URL_ENABLED`        | For debugging sentry /sentry-debug/                       | `False`                      |
| `SENTRY_ENVIRONMENT`              | Sets the environment                                      | _none_                       |
| `SENTRY_SAMPLE_RATE`              | Configures the sample rate for error events,              | `0.5`                        |
|                                   | in the range of 0.0 to 1.0                                |                              |
| `SENTRY_SEND_USER_DATA`           | When set certain personally identifiable information      | `False`                      |
|                                   | (PII) is added by active integrations                     |                              |

See [Sentry's official guide](https://docs.sentry.io/platforms/python/guides/django/) for further information on configuring Sentry for Django projects.

`.env` variables:

| Variable                  | Purpose                                            |
| ------------------------- | -------------------------------------------------- |
| `ROSETTA_CLIENT_BASE_URL` | Api used to query the data                         |
| `ROSETTA_CLIENT_KEY`      | Api key to query the data                          |
| `SENTRY_DSN`              | The project-specific identifier provided by Sentry |
