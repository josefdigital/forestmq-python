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
	python setup.py sdist
	twine upload dist/* --verbose