#! /usr/bin/env sh
set -e

# Start Gunicorn
echo "Starting Gunicorn..."
exec pipenv run gunicorn -k egg:meinheld#gunicorn_worker -c "$GUNICORN_CONF" "$APP_MODULE"