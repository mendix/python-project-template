PACKAGE_NAME := {{cookiecutter.package_name}}

.PHONY: install_lint_requirements
install_lint_requirements:
	poetry install --with lint

.PHONY: lint
lint: install_lint_requirements
	flake8 $(PACKAGE_NAME) tests
	black --check --diff $(PACKAGE_NAME) tests
	pylint $(PACKAGE_NAME) tests
	isort --check-only $(PACKAGE_NAME) tests
	mypy --ignore-missing-imports $(PACKAGE_NAME) tests

.PHONY: install_test_requirements
install_test_requirements:
	poetry install --with test

.PHONY: test
test: install_test_requirements
	pytest \
		--cov=$(PACKAGE_NAME) \
		--cov=tests \
		--cov-report=term-missing:skip-covered \
		tests

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf $(PACKAGE_NAME).egg-info
	rm -rf pip-wheel-metadata
	rm -rf dist
	rm -rf build
	find . -regex ".*__pycache__.*" -delete
	find . -regex "*.py[co]" -delete

.PHONY: build
build:
	poetry build

.PHONY: format
format:
	black $(PACKAGE_NAME) tests
	isort $(PACKAGE_NAME) tests
