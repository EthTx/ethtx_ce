FROM python:3.9

WORKDIR /app/

# Upgrade pip, install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Copy Pipfile* in case it doesn't exist in the repo
COPY ./app/Pipfile* /app/


COPY ./app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./app/start.sh  /start.sh
RUN chmod +x /start.sh

COPY ./app/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app/gunicorn_conf.py /gunicorn_conf.py

RUN bash -c "pipenv install --dev --deploy"

ARG GIT_URL
ENV GIT_URL=$GIT_URL

ARG GIT_SHA
ENV GIT_SHA=$GIT_SHA

ARG CI=1

COPY ./app /app
ENV PYTHONPATH=/app

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
