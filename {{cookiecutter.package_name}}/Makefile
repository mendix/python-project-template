.PHONY: install_lint_requirements
install_lint_requirements:
	pip3 install -e .[lint]

.PHONY: lint
lint: install_lint_requirements
	flake8 {{cookiecutter.package_name}} tests
	black --line-length=79 --check --diff {{cookiecutter.package_name}} tests
	{%- if cookiecutter.use_pylint == "y" %}
	pylint {{cookiecutter.package_name}} tests
	{%- endif%}
	{%- if cookiecutter.use_mypy == "y" %}
	mypy {{cookiecutter.package_name}}
	{%- endif%}

.PHONY: install_test_requirements
install_test_requirements:
	pip3 install -e .[test]

.PHONY: test
test: install_test_requirements
	pytest \
		--cov={{cookiecutter.package_name}} \
		--cov=tests \
		--cov-report=term-missing:skip-covered \
		tests

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf {{cookiecutter.package_name}}.egg-info
	rm -rf dist
	rm -rf build
	find . -regex ".*__pycache__.*" -delete
	find . -regex "*.py[co]" -delete

.PHONY: install_build_requirements
install_build_requirements:
	pip3 install -e .[build]

.PHONY: build
build: install_build_requirements
	python3 setup.py sdist bdist_wheel

.PHONY: format
format:
	black --line-length=79 {{cookiecutter.package_name}} tests
