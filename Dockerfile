FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app
ADD . /app
COPY Pip* /app/

COPY tmp/git_version /app/git_version

ARG CI=1
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install #--dev --system --deploy --ignore-pipfile

EXPOSE 5000

CMD cd /app && pipenv run gunicorn --workers 4 --max-requests 4000 --timeout 600 --bind :5000 wsgi:app
