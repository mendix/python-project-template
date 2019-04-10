.PHONY: install_lint_requirements
install_lint_requirements:
	pip3 install -e .[lint]

.PHONY: lint
lint: install_lint_requirements
	flake8 {{cookiecutter.package_name}} tests
	black --line-length=79 --check --diff {{cookiecutter.package_name}} tests

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
	rm -rf {{cookiecutter.package_name}}.egg-info
	find . -regex ".*__pycache__.*" -delete
	find . -regex "*.py[co]" -delete


.PHONY: format
format:
	black --line-length=79 {{cookiecutter.package_name}} tests
