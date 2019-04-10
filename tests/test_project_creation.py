"""Test Python project creation with `cookiecutter`.

This test module makes use of `pytest` fixtures and the `pytest-cookies`
fixture plugin (https://github.com/hackebrot/pytest-cookies). Therefore if
you encounter a `cookies` parameter in a test-function fear not, it is a
`cookiecutter` test fixture, injected by `pylint`.
This plugin makes it a lot more convenient to invoke `cookiecutter` than
calling it as an external process, having to programatically complete the
project generator wizard.
"""
import contextlib
import shutil


DEFAULT_PROJECT_NAME = "pymx"
EXPECTED_PROJECT_FILES = (
    DEFAULT_PROJECT_NAME,
    ".gitignore",
    "README.md",
    "setup.py",
    "tests",
)


@contextlib.contextmanager
def generate_temporary_project(cookies):
    try:
        result = cookies.bake()
        yield result
    finally:
        shutil.rmtree(str(result.project))


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
