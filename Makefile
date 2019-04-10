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
