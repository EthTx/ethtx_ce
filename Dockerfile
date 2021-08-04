FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app
ADD . /app
COPY Pip* /app/

ARG GIT_URL
ENV GIT_URL=$GIT_URL

ARG GIT_SHA
ENV GIT_SHA=$GIT_SHA

ARG CI=1
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install #--dev --system --deploy --ignore-pipfile

EXPOSE 5000

CMD cd /app && pipenv run gunicorn --workers 4 --max-requests 4000 --timeout 600 --bind :5000 wsgi:app
