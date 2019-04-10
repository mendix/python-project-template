.PHONY: install_lint_requirements
install_lint_requirements:
	pip3 install -e .[lint]

.PHONY: lint
lint: install_lint_requirements
	flake8 {{cookiecutter.package_name}} tests
	black --line-length=79 --check --diff {{cookiecutter.package_name}} tests
