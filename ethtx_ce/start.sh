#! /usr/bin/env sh
set -e

# Start Gunicorn
echo "Starting Gunicorn..."
exec pipenv run gunicorn -k gthread -c "$GUNICORN_CONF" "$APP_MODULE"