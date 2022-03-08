#! /usr/bin/env sh
set -e

# Start Gunicorn
echo "Starting Gunicorn --reload ..."
echo "GUNICORN_CONF: $GUNICORN_CONF"
echo "APP_MODULE: $APP_MODULE"
exec pipenv run gunicorn "--reload" -k egg:meinheld#gunicorn_worker -c "$GUNICORN_CONF" "$APP_MODULE"