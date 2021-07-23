

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-image:  ## Build all docker images
	docker build -t ethtx_ce .

run-database:  ## Run only a local database required for local development
	docker-compose up -d mongo mongo-express

populate-db: run-database ## Populate a local database with semantics specified in backup json files
	docker-compose build mongo-seed && docker-compose up mongo-seed && docker-compose rm mongo-seed

run-local:
	FLASK_APP=run.py FLASK_DEBUG=1 pipenv run flask run --host=0.0.0.0 --port 5000

run-prod:
	fuser -k 5000/tcp || true
	pipenv run gunicorn --workers 4 --max-requests 4000 --timeout 600 --bind :5000 wsgi:app

run-docker:
	fuser -k 5000/tcp || true
	docker-compose up -d

run-test-docker:
	docker run -it ethtx_ce make test

test:
	PYTHONPATH=. pipenv run python -m pytest --ignore=tests/providers .
