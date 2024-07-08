install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

package-reinstall:
	python3 -m pip install dist/*.whl --force-reinstall

lint:
	poetry run flake8 gendiff

gendiff-test:
	poetry run gendiff --help

gendiff:
	poetry run gendiff

test:
	poetry run python3 -m pytest tests

check:
	make test && make lint

test-coverage:
	poetry run pytest --cov=hexlet_python_package --cov-report xml

.PHONY: install build publish package-install package-reinstall lint gendiff gendiff-test test check