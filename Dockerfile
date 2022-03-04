FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

COPY Pipfile /app/

RUN pip install --upgrade pip && pip install pipenv

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./scripts/start.sh  /start.sh
RUN chmod +x /start.sh

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

RUN bash -c "pipenv install --dev --deploy"

ARG GIT_URL
ENV GIT_URL=$GIT_URL

ARG GIT_SHA
ENV GIT_SHA=$GIT_SHA

ARG CI=1

COPY . /app
ENV PYTHONPATH=/app

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
