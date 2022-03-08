help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-image:  ## Build all docker images
	docker build -t ethtx_ce ./ethtx_ce

get-git-version: ## Get git version
	./scripts/git_version_for_docker.sh

run-database:  ## Run only a local database required for local development
	docker-compose up -d mongo mongo-express

run-local:
	PYTHONPATH=./ethtx_ce/app FLASK_APP=ethtx_ce/app/app/wsgi.py FLASK_DEBUG=1 pipenv run flask run --host=0.0.0.0 --port 5000

run-prod:
	fuser -k 5000/tcp || true
	PYTHONPATH=./ethtx_ce/app pipenv run gunicorn --workers 4 --max-requests 4000 --timeout 600 --bind :5000 app.wsgi:app

run-docker:
	fuser -k 5000/tcp || true
	docker-compose up -d

test:
	PYTHONPATH=./ethtx_ce/app pipenv run python -m pytest ethtx_ce/app/app/tests/

test-all:
	PYTHONPATH=./ethtx_ce/app pipenv run python -m pytest .

setup:
	export PIPENV_PIPFILE=./ethtx_ce/app/Pipfile
	pipenv install --dev
	pipenv run pre-commit install
