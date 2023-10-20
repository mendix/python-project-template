POETRY ?= poetry
_RUN   ?= $(POETRY) run
PIP    ?= pip3
PYTEST ?= $(_RUN) pytest
FLAKE8 ?= $(_RUN) flake8
BLACK  ?= $(_RUN) black
PYLINT ?= $(_RUN) pylint
ISORT  ?= $(_RUN) isort
MYPY   ?= $(_RUN) mypy

COOKIECUTTER ?= cookiecutter

TESTS_DIR := tests

.PHONY: install_lint_requirements
install_lint_requirements:
	$(POETRY) install --with lint

.PHONY: lint
lint: install_lint_requirements
	$(FLAKE8) $(TESTS_DIR)
	$(BLACK) --check --diff $(TESTS_DIR)
	$(PYLINT) $(TESTS_DIR)
	$(ISORT) --check-only $(TESTS_DIR)
	$(MYPY) $(TESTS_DIR)

.PHONY: install_test_requirements
install_test_requirements:
	$(POETRY) install --with test

.PHONY: test
test: install_test_requirements
	$(PYTEST) $(PYTEST_OPTS) $(TESTS_DIR)

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf python_project_template.egg-info
	rm -rf pip-wheel-metadata
	find . -regex ".*__pycache__.*" -delete
	find . -regex "*.py[co]" -delete

.PHONY: format
format:
	$(BLACK) $(TESTS_DIR)
	$(ISORT) $(TESTS_DIR)

.PHONY: install
install:
	$(PIP) install .

TARGET_DIR ?= .

.PHONY: generate
generate: install
	$(COOKIECUTTER) -v . --output-dir="$(TARGET_DIR)"
