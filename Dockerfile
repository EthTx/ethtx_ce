FROM python:3.9

WORKDIR /app/

# Upgrade pip, install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Copy Pipfile* in case it doesn't exist in the repo
COPY Pipfile* /app/

COPY ./ethtx_ce/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./ethtx_ce/start.sh  /start.sh
RUN chmod +x /start.sh

COPY ./ethtx_ce/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./ethtx_ce/gunicorn_conf.py /gunicorn_conf.py

COPY Makefile /Makefile

RUN bash -c "pipenv install --dev --deploy"

ARG GIT_URL
ENV GIT_URL=$GIT_URL

ARG GIT_SHA
ENV GIT_SHA=$GIT_SHA

ARG CI=1

COPY ./ethtx_ce /app
ENV PYTHONPATH=/app

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
