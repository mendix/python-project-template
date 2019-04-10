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
