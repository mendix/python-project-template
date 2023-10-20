POETRY ?= poetry
PYTEST ?= poetry run pytest
FLAKE8 ?= poetry run flake8
BLACK  ?= poetry run black
PYLINT ?= poetry run pylint
ISORT  ?= poetry run isort
MYPY   ?= poetry run mypy

PACKAGE_NAME := {{cookiecutter.package_name}}
TESTS_DIR    := tests
ALL_SOURCE   := $(PACKAGE_NAME) $(TESTS_DIR)

.PHONY: install_lint_requirements
install_lint_requirements:
	$(POETRY) install --with lint

.PHONY: lint
lint: install_lint_requirements
	$(FLAKE8) $(ALL_SOURCE)
	$(BLACK) --check --diff $(ALL_SOURCE)
	$(PYLINT) $(ALL_SOURCE)
	$(ISORT) --check-only $(ALL_SOURCE)
	$(MYPY) $(ALL_SOURCE)

.PHONY: install_test_requirements
install_test_requirements:
	$(POETRY) install --with test

.PHONY: test
test: install_test_requirements
	$(PYTEST) $(PYTEST_OPTS) \
		--cov=$(PACKAGE_NAME) \
		--cov=$(TESTS_DIR) \
		--cov-report=term-missing:skip-covered \
		$(TESTS_DIR)

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
	$(POETRY) build

.PHONY: format
format:
	$(BLACK) $(ALL_SOURCE)
	$(ISORT) $(ALL_SOURCE)
