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
    check_output_in_result_dir,
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


def assert_successful_creation(result):
    assert result.project.isdir()
    assert result.exit_code == 0
    assert result.exception is None


def assert_expected_files_exist(result):
    created_files = [f.basename for f in result.project.listdir()]
    for fname in EXPECTED_PROJECT_FILES:
        assert fname in created_files


def test_default_project_creation(cookies):
    with generate_temporary_project(cookies) as result:
        assert_successful_creation(result)
        assert_expected_files_exist(result)


def assert_expected_lines_are_in_output(expected_lines, output):
    for line in expected_lines:
        assert line in output


EXPECTED_LINT_OUTPUT = (
    "pip3 install -e .[lint]",
    f"flake8 {DEFAULT_PROJECT_NAME} tests",
    f"black --line-length=79 --check --diff {DEFAULT_PROJECT_NAME} tests",
    "files would be left unchanged",
)


def test_linting(cookies):
    with generate_temporary_project(cookies) as result:
        output = check_output_in_result_dir("make lint", result)
        assert_expected_lines_are_in_output(EXPECTED_LINT_OUTPUT, output)


EXPECTED_TEST_OUTPUT = (
    "pip3 install -e .[test]",
    "test session starts",
    "files skipped due to complete coverage.",
)


def test_test_run(cookies):
    with generate_temporary_project(cookies) as result:
        output = check_output_in_result_dir("make test", result)
        assert_expected_lines_are_in_output(EXPECTED_TEST_OUTPUT, output)


EXPECTED_CLEANED_UP_FILE_PARTS = (
    ".coverage",
    ".pytest_cache",
    f"{DEFAULT_PROJECT_NAME}.egg-info",
    ".pyc",
    ".pyo",
    "__pycache__",
)


def assert_expected_files_cleaned_up(result):
    with inside_directory_of(result):
        for cleaned_up in EXPECTED_CLEANED_UP_FILE_PARTS:
            for filename in glob.glob("./**", recursive=True):
                assert cleaned_up not in filename


def test_cleaning(cookies):
    with generate_temporary_project(cookies) as result:
        check_output_in_result_dir("make test", result)
        check_output_in_result_dir("make clean", result)

        assert_expected_files_cleaned_up(result)
