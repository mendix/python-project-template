.PHONY: install_lint_requirements
install_lint_requirements:
	poetry install --with lint

.PHONY: lint
lint: install_lint_requirements
	flake8 tests
	black --check --diff tests
	pylint tests
	isort --check-only tests
	mypy tests

.PHONY: install_test_requirements
install_test_requirements:
	poetry install --with test

.PHONY: test
test: install_test_requirements
	pytest tests

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
	black tests
	isort tests

.PHONY: install
install:
	pip3 install .

TARGET_DIR := .

.PHONY: generate
generate: install
	cookiecutter -v . --output-dir="$(TARGET_DIR)"
