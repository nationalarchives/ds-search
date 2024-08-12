# TNA Python Flask Application

## Quickstart

```sh
# Build and start the container
docker compose up -d

# Install Node modules
npm install

# Create a static assets directory
mkdir app/static/assets

# Copy in the TNA Frontend static assets
cp -r node_modules/@nationalarchives/frontend/nationalarchives/assets/* app/static/assets
```

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

| Variable                 | Purpose                                                   | Default                      |
| ------------------------ | --------------------------------------------------------- | ---------------------------- |
| `DJANGO_SETTINGS_MODULE` | The configuration to use                                  | `config.settings.production` |
| `DEBUG`                  | If true, allow debugging                                  | `False`                      |
| `COOKIE_DOMAIN`          | The domain to save cookie preferences against             | _none_                       |
| `DATABASE_NAME`          | The name of the Postgres database                         | _none_                       |
| `DATABASE_USER`          | The username needed to access the Postgres database       | _none_                       |
| `DATABASE_PASSWORD`      | The password needed to access the Postgres database       | _none_                       |
| `DATABASE_HOST`          | The Postgres database host                                | _none_                       |
| `DATABASE_PORT`          | The Postgres database port                                | `5432`                       |
| `CSP_IMG_SRC`            | A comma separated list of CSP rules for `img-src`         | `'self'`                     |
| `CSP_SCRIPT_SRC`         | A comma separated list of CSP rules for `script-src`      | `'self'`                     |
| `CSP_SCRIPT_SRC_ELEM`    | A comma separated list of CSP rules for `script-src-elem` | `'self'`                     |
| `CSP_STYLE_SRC`          | A comma separated list of CSP rules for `style-src`       | `'self'`                     |
| `CSP_STYLE_SRC_ELEM`     | A comma separated list of CSP rules for `style-src-elem`  | `'self'`                     |
| `CSP_FONT_SRC`           | A comma separated list of CSP rules for `font-src`        | `'self'`                     |
| `CSP_CONNECT_SRC`        | A comma separated list of CSP rules for `connect-src`     | `'self'`                     |
| `CSP_MEDIA_SRC`          | A comma separated list of CSP rules for `media-src`       | `'self'`                     |
| `CSP_WORKER_SRC`         | A comma separated list of CSP rules for `worker-src`      | `'self'`                     |
| `CSP_FRAME_SRC`          | A comma separated list of CSP rules for `frame-src`       | `'self'`                     |
| `GA4_ID`                 | The Google Analytics 4 ID                                 | _none_                       |
