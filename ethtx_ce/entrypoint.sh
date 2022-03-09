#!/usr/bin/env sh
set -e

echo "ethtx_ce entrypoint.sh"

if [ -f /app/app/wsgi.py ]; then
    DEFAULT_MODULE_NAME=app.wsgi
elif [ -f /app/wsgi.py ]; then
    DEFAULT_MODULE_NAME=wsgi
fi
echo "DEFAULT_MODULE_NAME: $DEFAULT_MODULE_NAME"

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
echo "MODULE_NAME: $MODULE_NAME"
echo "VARIABLE_NAME: $VARIABLE_NAME"

export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}
echo "APP_MODULE: $APP_MODULE"

if [ -f /app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
elif [ -f /app/app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
echo "GUNICORN_CONF: $GUNICORN_CONF"

exec "$@"