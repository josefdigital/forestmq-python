test:
	pipenv run pytest -vvvv

lint:
	pipenv run pylint forestmq

docs:
	make -C docs html

install:
	pipenv install
	pipenv install --dev

# Tox is only for local development (we use github actions in CI)
tox:
	pipenv run tox

release:
	pipenv run python -m build
	pipenv run python -m twine upload dist/* --verbose

docker_compose_run:
	docker compose -f docker-compose.yaml up