"""Test Python project creation with `cookiecutter`.

This test module makes use of `pytest` fixtures and the `pytest-cookies`
fixture plugin (https://github.com/hackebrot/pytest-cookies). Therefore if
you encounter a `cookies` parameter in a test-function fear not, it is a
`cookiecutter` test fixture, injected by `pylint`.
This plugin makes it a lot more convenient to invoke `cookiecutter` than
calling it as an external process, having to programatically complete the
project generator wizard.
"""
import glob

from .util import (
    check_output_in_result_directory,
    generate_temporary_project,
    inside_directory_of,
)


DEFAULT_PROJECT_NAME = "pymx"
EXPECTED_PROJECT_FILES = (
    DEFAULT_PROJECT_NAME,
    ".gitignore",
    "README.md",
    "setup.py",
    "tests",
)


def assert_project_creation_is_successful(result):
    assert result.project.isdir()
    assert result.exit_code == 0
    assert result.exception is None


def assert_expected_files_are_created(result):
    created_files = [f.basename for f in result.project.listdir()]
    for fname in EXPECTED_PROJECT_FILES:
        assert fname in created_files


def test_default_project_creation(cookies):
    with generate_temporary_project(cookies) as result:
        assert_project_creation_is_successful(result)
        assert_expected_files_are_created(result)


EXPECTED_LINT_OUTPUT = (
    "pip3 install -e .[lint]",
    f"flake8 {DEFAULT_PROJECT_NAME} tests",
    f"black --line-length=79 --check --diff {DEFAULT_PROJECT_NAME} tests",
    "files would be left unchanged",
)


def test_linting(cookies):
    with generate_temporary_project(cookies) as result:
        output = check_output_in_result_directory("make lint", result)
        for line in EXPECTED_LINT_OUTPUT:
            assert line in output


EXPECTED_TEST_OUTPUT = (
    "pip3 install -e .[test]",
    "test session starts",
    "files skipped due to complete coverage.",
)


def test_test_run(cookies):
    with generate_temporary_project(cookies) as result:
        output = check_output_in_result_directory("make test", result)
        for line in EXPECTED_TEST_OUTPUT:
            assert line in output


EXPECTED_CLEANED_UP_FILE_PARTS = (
    ".coverage",
    ".pytest_cache",
    f"{DEFAULT_PROJECT_NAME}.egg-info",
    ".pyc",
    ".pyo",
    "__pycache__",
)


def test_cleaning(cookies):
    with generate_temporary_project(cookies) as result:
        check_output_in_result_directory("make test", result)
        check_output_in_result_directory("make clean", result)
        with inside_directory_of(result):
            for cleaned_up in EXPECTED_CLEANED_UP_FILE_PARTS:
                for filename in glob.glob('./**', recursive=True):
                    assert cleaned_up not in filename
