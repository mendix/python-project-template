{%- if cookiecutter.build_system == "poetry" -%}
POETRY ?= poetry
_RUN   ?= $(POETRY) run
{% set runner = "$(_RUN) " %}
{%- else -%}
PIP    ?= pip3
PYTHON ?= python3
{% set runner = "" %}
{%- endif -%}
PYTEST ?= {{ runner  }}pytest
FLAKE8 ?= {{ runner  }}flake8
BLACK  ?= {{ runner  }}black
PYLINT ?= {{ runner  }}pylint
ISORT  ?= {{ runner  }}isort
MYPY   ?= {{ runner  }}mypy

PACKAGE_NAME := {{cookiecutter.package_name}}
TESTS_DIR    := tests
ALL_SOURCE   := $(PACKAGE_NAME) $(TESTS_DIR)

.PHONY: install_lint_requirements
install_lint_requirements:
{%- if cookiecutter.build_system == "poetry" %}
	$(POETRY) install --with lint
{%- else %}
	$(PIP) install -e .[lint]
{%- endif %}

.PHONY: lint
lint: install_lint_requirements
	$(FLAKE8) $(ALL_SOURCE)
	$(BLACK) --check --diff $(ALL_SOURCE)
	$(PYLINT) $(ALL_SOURCE)
	$(ISORT) --check-only $(ALL_SOURCE)
	$(MYPY) $(ALL_SOURCE)

.PHONY: install_test_requirements
install_test_requirements:
{%- if cookiecutter.build_system == "poetry" %}
	$(POETRY) install --with test
{%- else %}
	$(PIP) install -e .[test]
{%- endif %}

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
{%- if cookiecutter.build_system == "poetry" %}
	$(POETRY) build
{%- else %}
	$(PIP) install -e .[build]
	$(PYTHON) -m build
{%- endif %}

.PHONY: format
format: install_lint_requirements
	$(BLACK) $(ALL_SOURCE)
	$(ISORT) $(ALL_SOURCE)
