#! /usr/bin/env sh
set -e

# Start Gunicorn
echo "Starting Gunicorn ..."
echo "GUNICORN_CONF: $GUNICORN_CONF"
echo "APP_MODULE: $APP_MODULE"

exec pipenv run gunicorn -k egg:meinheld#gunicorn_worker -c "$GUNICORN_CONF" "$APP_MODULE"