"""Test Python project creation with `cookiecutter`.

This test module makes use of `pytest` fixtures and the `pytest-cookies`
fixture plugin (https://github.com/hackebrot/pytest-cookies). Therefore if
you encounter a `cookies` parameter in a test-function fear not, it is a
`cookiecutter` test fixture, injected by `pytest`.
This plugin makes it a lot more convenient to invoke `cookiecutter` than
calling it as an external process, having to programatically complete the
project generator wizard.
"""
import glob
from collections.abc import Sequence

from pytest_cookies.plugin import Cookies, Result

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
    "pylintrc",
)


def assert_successful_creation(result: Result) -> None:
    assert result.project.isdir()
    assert result.exit_code == 0
    assert result.exception is None


def assert_expected_files_exist(result: Result, files: Sequence[str]) -> None:
    created_files = [f.basename for f in result.project.listdir()]
    for fname in files:
        assert fname in created_files


def test_default_project_creation(cookies: Cookies) -> None:
    with generate_temporary_project(cookies) as result:
        assert_successful_creation(result)
        assert_expected_files_exist(result, files=EXPECTED_PROJECT_FILES)


def test_project_creation_with_invalid_name_fails(cookies: Cookies) -> None:
    result = cookies.bake(extra_context={"package_name": "Foo-Bar"})
    assert result.exit_code != 0


def assert_expected_files_do_not_exist(
    result: Result, files: Sequence[str]
) -> None:
    with inside_directory_of(result):
        for cleaned_up in files:
            for filename in glob.glob("./**", recursive=True):
                assert cleaned_up not in filename


EXPECTED_PROJECT_FILES_NO_PYLINT = tuple(
    file_name
    for file_name in EXPECTED_PROJECT_FILES
    if file_name != "pylintrc"
)
NO_PLINT = {"use_pylint": "n"}


def test_project_creation_without_pylint(cookies: Cookies) -> None:
    with generate_temporary_project(cookies, extra_context=NO_PLINT) as result:
        assert_successful_creation(result)
        assert_expected_files_exist(
            result, files=EXPECTED_PROJECT_FILES_NO_PYLINT
        )
        assert_expected_files_do_not_exist(result, files=("pylintrc",))


def assert_expected_lines_are_in_output(
    expected_lines: Sequence[str],
    output: str,
) -> None:
    for line in expected_lines:
        assert line in output


FILES_TO_CHECK_FORMAT = f"{DEFAULT_PROJECT_NAME} tests setup.py"
BLACK_OUTPUT = f"black --line-length=79 --check --diff {FILES_TO_CHECK_FORMAT}"
PYLINT_OUTPUT_1 = f"pylint {DEFAULT_PROJECT_NAME} tests"
PYLINT_OUTPUT_2 = "Your code has been rated at 10.00/10"
ISORT_OUTPUT = f"isort --check-only {DEFAULT_PROJECT_NAME} tests setup.py"
MYPY_OUTPUT = f"mypy --ignore-missing-imports {DEFAULT_PROJECT_NAME} tests"
EXPECTED_LINT_OUTPUT = (
    "pip3 install -e .[lint]",
    f"flake8 {DEFAULT_PROJECT_NAME} tests",
    "files would be left unchanged",
    BLACK_OUTPUT,
    PYLINT_OUTPUT_1,
    PYLINT_OUTPUT_2,
    ISORT_OUTPUT,
    MYPY_OUTPUT,
)


def test_linting(cookies: Cookies) -> None:
    with generate_temporary_project(cookies) as result:
        output = check_output_in_result_dir("make lint", result)
        assert_expected_lines_are_in_output(EXPECTED_LINT_OUTPUT, output)


def test_linting_without_pylint(cookies: Cookies) -> None:
    with generate_temporary_project(cookies, extra_context=NO_PLINT) as result:
        output = check_output_in_result_dir("make lint", result)
        assert PYLINT_OUTPUT_1 not in output
        assert PYLINT_OUTPUT_2 not in output


EXPECTED_TEST_OUTPUT = (
    "pip3 install -e .[test]",
    "test session starts",
    "files skipped due to complete coverage.",
)


def test_test_run(cookies: Cookies) -> None:
    with generate_temporary_project(cookies) as result:
        output = check_output_in_result_dir("make test", result)
        assert_expected_lines_are_in_output(EXPECTED_TEST_OUTPUT, output)


EXPECTED_CLEANED_UP_FILE_PARTS = (
    ".coverage",
    ".pytest_cache",
    ".mypy_cache",
    f"{DEFAULT_PROJECT_NAME}.egg-info",
    "pip-wheel-metadata",
    ".pyc",
    ".pyo",
    "__pycache__",
    "build",
    "dist",
    ".tar.gz",
    ".whl",
)


def test_cleaning(cookies: Cookies) -> None:
    with generate_temporary_project(cookies) as result:
        check_output_in_result_dir("make lint", result)
        check_output_in_result_dir("make test", result)
        check_output_in_result_dir("make build", result)
        check_output_in_result_dir("make clean", result)

        assert_expected_files_do_not_exist(
            result, files=EXPECTED_CLEANED_UP_FILE_PARTS
        )


def test_clean_can_be_executed_in_empty_project_dir(cookies: Cookies) -> None:
    with generate_temporary_project(cookies) as result:
        check_output_in_result_dir("make clean", result)


EXPECTED_FORMAT_OUTPUT = (
    f"black --line-length=79 {DEFAULT_PROJECT_NAME} tests setup.py",
    "files left unchanged",
    f"isort {DEFAULT_PROJECT_NAME} tests setup.py",
)


def test_formatting(cookies: Cookies) -> None:
    with generate_temporary_project(cookies) as result:
        output = check_output_in_result_dir("make format", result)
        assert_expected_lines_are_in_output(EXPECTED_FORMAT_OUTPUT, output)


EXPECTED_BUILD_PATTERNS = ("./dist/*.tar.gz", "./dist/*.whl")


def test_build(cookies: Cookies) -> None:
    with generate_temporary_project(cookies) as result:
        check_output_in_result_dir("make build", result)
        with inside_directory_of(result):
            for pattern in EXPECTED_BUILD_PATTERNS:
                assert glob.glob(pattern)
